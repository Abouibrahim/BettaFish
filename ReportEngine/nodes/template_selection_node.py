"""
Template selection node
Selects the most appropriate report template based on query content and available templates
"""

import os
import json
from typing import Dict, Any, List, Optional
from loguru import logger

from .base_node import BaseNode
from ..prompts import SYSTEM_PROMPT_TEMPLATE_SELECTION


class TemplateSelectionNode(BaseNode):
    """Template selection processing node"""

    def __init__(self, llm_client, template_dir: str = "ReportEngine/report_template"):
        """
        Initialize template selection node

        Args:
            llm_client: LLM client
            template_dir: Template directory path
        """
        super().__init__(llm_client, "TemplateSelectionNode")
        self.template_dir = template_dir
        
    def run(self, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Execute template selection

        Args:
            input_data: Dictionary containing query and report content
                - query: Original query
                - reports: List of reports from three sub-agents
                - forum_logs: Forum log content

        Returns:
            Selected template information
        """
        logger.info("Starting template selection...")

        query = input_data.get('query', '')
        reports = input_data.get('reports', [])
        forum_logs = input_data.get('forum_logs', '')

        # Get available templates
        available_templates = self._get_available_templates()

        if not available_templates:
            logger.info("No preset templates found, using built-in default template")
            return self._get_fallback_template()

        # Use LLM for template selection
        try:
            llm_result = self._llm_template_selection(query, reports, forum_logs, available_templates)
            if llm_result:
                return llm_result
        except Exception as e:
            logger.exception(f"LLM template selection failed: {str(e)}")

        # If LLM selection fails, use fallback
        return self._get_fallback_template()
    

    
    def _llm_template_selection(self, query: str, reports: List[Any], forum_logs: str,
                              available_templates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Use LLM for template selection"""
        logger.info("Attempting to use LLM for template selection...")

        # Build template list
        template_list = "\n".join([f"- {t['name']}: {t['description']}" for t in available_templates])

        # Build reports content summary
        reports_summary = ""
        if reports:
            reports_summary = "\n\n=== Analysis Engine Report Content ===\n"
            for i, report in enumerate(reports, 1):
                # Get report content, supporting different data formats
                if isinstance(report, dict):
                    content = report.get('content', str(report))
                elif hasattr(report, 'content'):
                    content = report.content
                else:
                    content = str(report)

                # Truncate overly long content, keep first 1000 characters
                if len(content) > 1000:
                    content = content[:1000] + "...(content truncated)"

                reports_summary += f"\nReport {i} content:\n{content}\n"

        # Build forum log summary
        forum_summary = ""
        if forum_logs and forum_logs.strip():
            forum_summary = "\n\n=== Discussion Content from Three Engines ===\n"
            # Truncate overly long log content, keep first 800 characters
            if len(forum_logs) > 800:
                forum_content = forum_logs[:800] + "...(discussion content truncated)"
            else:
                forum_content = forum_logs
            forum_summary += forum_content

        user_message = f"""Query content: {query}

Number of reports: {len(reports)} analysis engine reports
Forum logs: {'Yes' if forum_logs else 'No'}
{reports_summary}{forum_summary}

Available templates:
{template_list}

Based on the query content, report content, and forum logs, please select the most appropriate template."""

        # Call LLM
        response = self.llm_client.stream_invoke_to_string(SYSTEM_PROMPT_TEMPLATE_SELECTION, user_message)

        # Check if response is empty
        if not response or not response.strip():
            logger.error("LLM returned empty response")
            return None

        logger.info(f"LLM raw response: {response}")

        # Try to parse JSON response
        try:
            # Clean response text
            cleaned_response = self._clean_llm_response(response)
            result = json.loads(cleaned_response)

            # Verify selected template exists
            selected_template_name = result.get('template_name', '')
            for template in available_templates:
                if template['name'] == selected_template_name or selected_template_name in template['name']:
                    logger.info(f"LLM selected template: {selected_template_name}")
                    return {
                        'template_name': template['name'],
                        'template_content': template['content'],
                        'selection_reason': result.get('selection_reason', 'LLM intelligent selection')
                    }

            logger.error(f"LLM selected template does not exist: {selected_template_name}")
            return None

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            # Try to extract template info from text response
            return self._extract_template_from_text(response, available_templates)
    
    def _clean_llm_response(self, response: str) -> str:
        """Clean LLM response"""
        # Remove possible markdown code block markers
        if '```json' in response:
            response = response.split('```json')[1].split('```')[0]
        elif '```' in response:
            response = response.split('```')[1].split('```')[0]

        # Remove leading and trailing whitespace
        response = response.strip()

        return response

    def _extract_template_from_text(self, response: str, available_templates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Extract template info from text response"""
        logger.info("Attempting to extract template info from text response")

        # Search for template names in response
        for template in available_templates:
            template_name_variants = [
                template['name'],
                template['name'].replace('.md', ''),
                template['name'].replace('template', ''),
            ]

            for variant in template_name_variants:
                if variant in response:
                    logger.info(f"Found template in response: {template['name']}")
                    return {
                        'template_name': template['name'],
                        'template_content': template['content'],
                        'selection_reason': 'Extracted from text response'
                    }

        return None

    def _get_available_templates(self) -> List[Dict[str, Any]]:
        """Get list of available templates"""
        templates = []

        if not os.path.exists(self.template_dir):
            logger.error(f"Template directory does not exist: {self.template_dir}")
            return templates

        # Find all markdown template files
        for filename in os.listdir(self.template_dir):
            if filename.endswith('.md'):
                template_path = os.path.join(self.template_dir, filename)
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    template_name = filename.replace('.md', '')
                    description = self._extract_template_description(template_name)

                    templates.append({
                        'name': template_name,
                        'path': template_path,
                        'content': content,
                        'description': description
                    })
                except Exception as e:
                    logger.exception(f"Failed to read template file {filename}: {str(e)}")

        return templates

    def _extract_template_description(self, template_name: str) -> str:
        """Generate description based on template name"""
        if 'brand' in template_name or 'reputation' in template_name:
            return "Suitable for enterprise brand reputation and image analysis"
        elif 'competition' in template_name or 'market' in template_name:
            return "Suitable for market competition landscape and competitor analysis"
        elif 'daily' in template_name or 'periodic' in template_name:
            return "Suitable for daily monitoring and periodic reporting"
        elif 'policy' in template_name or 'industry' in template_name:
            return "Suitable for policy impact and industry dynamic analysis"
        elif 'hotspot' in template_name or 'social' in template_name:
            return "Suitable for social hotspot and public event analysis"
        elif 'emergency' in template_name or 'crisis' in template_name:
            return "Suitable for emergency events and crisis management"

        return "General report template"



    def _get_fallback_template(self) -> Dict[str, Any]:
        """Get fallback default template (empty template, let LLM freestyle)"""
        logger.info("Suitable template not found, using empty template to let LLM freestyle")

        return {
            'template_name': 'Freestyle Template',
            'template_content': '',
            'selection_reason': 'Suitable preset template not found, letting LLM design report structure based on content'
        }

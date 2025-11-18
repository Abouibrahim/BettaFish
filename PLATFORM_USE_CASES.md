# BettaFish Platform - Practical Use Cases Guide

This guide provides step-by-step instructions for the most valuable real-world applications of the BettaFish public opinion analysis platform.

---

## Use Case 1: Brand Crisis Monitoring & Early Warning

**Goal**: Detect negative sentiment spikes early to prevent PR disasters

### Step-by-Step Process

1. **Initial Setup**
   ```bash
   # Ensure environment is ready
   conda activate bettafish
   python app.py
   ```

2. **Configure Crawler for Continuous Monitoring**
   ```bash
   cd MindSpider
   # Set up database
   python main.py --setup

   # Extract current hot topics about your brand
   python main.py --broad-topic

   # Run deep sentiment crawling for specific platforms
   python main.py --deep-sentiment --platforms wb xhs dy
   ```

3. **Submit Analysis Query via Web Interface**
   - Navigate to `http://localhost:5000`
   - Enter query: *"Analyze recent sentiment about [BRAND_NAME] on social media, identify negative sentiment trends and potential PR risks"*
   - Click "Start Analysis"

4. **What Happens Behind the Scenes**
   - **Insight Agent**: Mines your sentiment database for historical patterns
   - **Media Agent**: Analyzes video/image content from Douyin, Kuaishou
   - **Query Agent**: Searches news and social media for recent mentions
   - **Forum Engine**: Agents debate significance of findings
   - **Report Agent**: Generates crisis assessment report

5. **Review Generated Report**
   - Report saved to `final_reports/` directory
   - Look for:
     - Sentiment trend graphs (positive/negative/neutral over time)
     - Key negative themes and complaints
     - Influencer amplification analysis
     - Crisis severity assessment
     - Recommended response actions

6. **Set Up Automated Monitoring** (Optional)
   - Schedule daily crawler runs via cron/scheduled tasks
   - Set sentiment threshold alerts
   - Monitor `logs/forum.log` for agent discussions flagging concerns

**Best Practices**:
- Run crawler daily during normal times, hourly during active campaigns
- Maintain 30-day rolling sentiment database for trend analysis
- Compare current sentiment against historical baseline

---

## Use Case 2: Product Launch Impact Analysis

**Goal**: Measure public reception and sentiment after launching a new product

### Step-by-Step Process

1. **Pre-Launch Baseline Collection** (1 week before launch)
   ```bash
   cd MindSpider
   # Collect baseline sentiment about product category
   python main.py --deep-sentiment --platforms xhs dy wb tb
   ```

2. **Post-Launch Deep Crawl** (Day 1, 3, 7, 14, 30 after launch)
   ```bash
   # Capture specific date's discussions
   python main.py --complete --date 2024-01-20
   ```

3. **Submit Comprehensive Analysis Query**
   - Query: *"Analyze public reaction to [PRODUCT_NAME] launch. Compare sentiment before and after launch date [DATE]. Identify key praise points, complaints, and unexpected user behaviors. Include multimodal content analysis from unboxing videos."*

4. **Agent Workflow**
   - **Insight Agent**: Compares pre/post launch sentiment distributions
   - **Media Agent**: Analyzes unboxing videos, product demo content
   - **Query Agent**: Tracks news coverage and influencer reviews
   - **Forum Engine**: Agents debate whether reception meets expectations
   - **Report Agent**: Generates launch performance report

5. **Extract Actionable Insights**
   - Review report sections:
     - **Sentiment Trajectory**: Day-by-day sentiment evolution
     - **Feature Reception**: Which features users love/hate
     - **Comparison Analysis**: vs. competitor products
     - **User Pain Points**: Common complaints requiring fixes
     - **Viral Moments**: Content that drove organic sharing
     - **Influencer Impact**: Which KOLs drove most engagement

6. **Feed Insights Back to Product Team**
   - Export data from database for deeper analysis:
   ```python
   # Custom query example
   from MindSpider.schema import SentimentData
   # Query high-engagement negative posts
   negative_viral = session.query(SentimentData).filter(
       SentimentData.sentiment == 'negative',
       SentimentData.engagement_score > threshold
   ).all()
   ```

**Key Metrics to Track**:
- Net sentiment score (positive % - negative %)
- Sentiment velocity (rate of change)
- Topic share-of-voice vs. competitors
- Influencer amplification coefficient

---

## Use Case 3: Competitive Intelligence Gathering

**Goal**: Monitor competitors' market positioning, product reception, and strategic moves

### Step-by-Step Process

1. **Configure Multi-Brand Monitoring**
   ```bash
   # Edit crawler config to track multiple brands
   cd MindSpider
   # Run broad topic extraction for competitive landscape
   python main.py --broad-topic
   ```

2. **Submit Competitive Analysis Query**
   - Query: *"Compare public sentiment and discussion topics about [YOUR_BRAND], [COMPETITOR_1], [COMPETITOR_2], and [COMPETITOR_3]. Identify their strengths, weaknesses, and unique selling propositions as perceived by consumers."*

3. **Deep Dive on Specific Competitor Moves**
   - Query: *"[COMPETITOR_NAME] recently announced [EVENT/PRODUCT]. Analyze public reaction, identify concerns consumers have, and assess potential market impact."*

4. **Agent Collaboration**
   - **Insight Agent**: Analyzes historical competitive sentiment trends
   - **Media Agent**: Compares video marketing strategies and effectiveness
   - **Query Agent**: Tracks news announcements and press coverage
   - **Forum Engine**: Agents debate competitive threats and opportunities

5. **Strategic Intelligence Report**
   - Report includes:
     - **Competitive Positioning Map**: Sentiment and topic clustering
     - **Share of Voice Analysis**: Discussion volume by brand
     - **Perception Gap Analysis**: Where competitors lead/lag
     - **Unmet Needs**: Consumer pain points no one is addressing
     - **Strategic Recommendations**: Opportunities to differentiate

6. **Set Up Ongoing Competitive Monitoring**
   - Schedule weekly competitive intelligence reports
   - Track competitor product launches, campaigns, crises
   - Monitor keyword trends indicating market shifts

**Advanced Techniques**:
- Use custom business data integration for internal sales data correlation
- Track competitor employee sentiment on workplace platforms
- Monitor supply chain and partnership announcements

---

## Use Case 4: Social/Political Trend Forecasting

**Goal**: Understand public opinion evolution on social issues to predict policy impacts or social movements

### Step-by-Step Process

1. **Define Trend Monitoring Topics**
   - Example topics: sustainability, privacy, regulation, social justice

2. **Historical Data Collection**
   ```bash
   cd MindSpider
   # Collect 90-day historical data
   python main.py --complete --date 2024-10-01
   python main.py --complete --date 2024-10-15
   # ... continue for desired date range
   ```

3. **Submit Trend Analysis Query**
   - Query: *"Analyze public opinion evolution on [TOPIC] over the past 90 days. Identify sentiment shifts, emerging sub-topics, influential voices, and predict likely future trends. Include analysis of mainstream news vs. grassroots social media discussion."*

4. **Multi-Source Intelligence Gathering**
   - **Insight Agent**: Identifies sentiment inflection points in database
   - **Media Agent**: Analyzes visual content framing (protest videos, infographics)
   - **Query Agent**: Tracks mainstream media narrative vs. social media reality
   - **Forum Engine**: Agents debate whether trends will accelerate or fade

5. **Predictive Report Analysis**
   - Report sections:
     - **Timeline of Key Events**: What triggered sentiment shifts
     - **Narrative Evolution**: How framing changed over time
     - **Echo Chamber Analysis**: Are opinions polarizing?
     - **Influencer Network Map**: Who's driving the conversation
     - **Predictive Indicators**: Leading signals for future movements
     - **Policy Impact Assessment**: Likelihood of regulatory response

6. **Create Trend Dashboard** (Optional)
   - Extract time-series data for visualization:
   ```python
   # Example: Export daily sentiment scores
   import pandas as pd
   from MindSpider.schema import SentimentData

   data = session.query(
       SentimentData.created_date,
       SentimentData.sentiment,
       func.count(SentimentData.id)
   ).filter(
       SentimentData.topic.contains('your_topic')
   ).group_by(
       SentimentData.created_date,
       SentimentData.sentiment
   ).all()

   df = pd.DataFrame(data)
   # Create visualization with your preferred tool
   ```

**Use Cases**:
- Government: Public policy sentiment assessment
- NGOs: Social movement strength evaluation
- Corporations: Regulatory risk monitoring
- Media: Emerging story identification

---

## Use Case 5: Influencer Campaign Effectiveness Measurement

**Goal**: Evaluate ROI of influencer marketing campaigns and identify best-performing collaborations

### Step-by-Step Process

1. **Pre-Campaign Baseline**
   ```bash
   cd MindSpider
   # Collect baseline brand sentiment
   python main.py --deep-sentiment --platforms xhs dy ks
   ```

2. **During Campaign: Track Influencer Content**
   - Note specific influencer posts/videos and publication dates
   - Run targeted crawls after each major influencer post:
   ```bash
   python main.py --complete --date 2024-01-25
   ```

3. **Submit Campaign Analysis Query**
   - Query: *"Analyze the impact of our influencer marketing campaign featuring [INFLUENCER_1], [INFLUENCER_2], [INFLUENCER_3]. Measure sentiment change, engagement patterns, conversion discussion (purchase intent mentions), and identify which influencer drove most authentic engagement vs. superficial comments."*

4. **Multi-Modal Campaign Assessment**
   - **Insight Agent**: Compares pre/during/post campaign sentiment
   - **Media Agent**: Analyzes video content quality, comment authenticity
   - **Query Agent**: Tracks campaign reach beyond original posts
   - **Forum Engine**: Agents debate which influencers delivered real value

5. **Campaign Performance Report**
   - Key metrics included:
     - **Reach Analysis**: Primary vs. secondary engagement
     - **Sentiment Lift**: Pre vs. post campaign sentiment improvement
     - **Authenticity Score**: Genuine comments vs. bot/paid comments
     - **Purchase Intent Signals**: Comments mentioning buying/wanting product
     - **Cost-Per-Sentiment-Point**: ROI calculation by influencer
     - **Halo Effect**: Did campaign improve overall brand perception?
     - **Influencer Ranking**: Best to worst performers with justification

6. **Optimize Future Campaigns**
   - Identify influencer characteristics correlating with high authenticity
   - Determine optimal posting times and content formats
   - Build influencer effectiveness database for future selection

**Advanced Analysis**:
- Sentiment analysis on influencer's audience comments
- Compare macro vs. micro vs. nano influencer effectiveness
- Track long-term brand lift (30/60/90 days post-campaign)

---

## Use Case 6: Customer Experience & Pain Point Analysis

**Goal**: Deep dive into customer complaints and satisfaction to improve products/services

### Step-by-Step Process

1. **Comprehensive Customer Voice Collection**
   ```bash
   cd MindSpider
   # Focus on review and forum platforms
   python main.py --deep-sentiment --platforms xhs tb jd dy
   ```

2. **Submit Customer Experience Query**
   - Query: *"Perform deep analysis of customer feedback about [PRODUCT/SERVICE]. Identify top pain points, frequency of each issue, emotional intensity, and patterns in negative experiences. Also identify unexpected positive use cases and moments of delight."*

3. **Agent Deep Dive**
   - **Insight Agent**: Clusters complaints into categories, tracks frequency trends
   - **Media Agent**: Analyzes complaint videos (product defects, unboxing disappointments)
   - **Query Agent**: Finds support forum discussions and resolution patterns
   - **Forum Engine**: Agents prioritize which issues are most critical

4. **Customer Experience Report**
   - Report structure:
     - **Pain Point Hierarchy**: Issues ranked by frequency × severity
     - **Customer Journey Pain Points**: Problems by stage (purchase, setup, use, support)
     - **Root Cause Analysis**: Why issues occur (design flaw, unclear instructions, etc.)
     - **Emotional Impact**: Which issues cause most frustration
     - **Resolution Effectiveness**: How well support handles each issue
     - **Hidden Delights**: Unexpected positive features customers love
     - **Feature Request Patterns**: What customers want added

5. **Create Actionable Issue Database**
   ```python
   # Query specific issue types
   from MindSpider.schema import SentimentData

   critical_issues = session.query(SentimentData).filter(
       SentimentData.sentiment == 'negative',
       SentimentData.content.contains('问题|故障|投诉|退款')  # Issue keywords
   ).order_by(SentimentData.engagement_score.desc()).limit(100).all()

   # Export for product team review
   ```

6. **Feed into Product Roadmap**
   - Prioritize fixes based on complaint frequency and sentiment impact
   - Identify quick wins (high-impact, low-effort fixes)
   - Design solutions for top 5 pain points
   - Measure sentiment improvement after each fix deployment

**Integration Options**:
- Connect to your CRM/support ticket system (custom tool in InsightEngine)
- Correlate social complaints with internal support tickets
- Track complaint resolution effectiveness

---

## Use Case 7: Market Research & Consumer Trend Discovery

**Goal**: Identify emerging consumer preferences and unmet market needs

### Step-by-Step Process

1. **Broad Market Scanning**
   ```bash
   cd MindSpider
   # Extract current hot topics in your industry
   python main.py --broad-topic
   ```

2. **Submit Exploratory Research Query**
   - Query: *"Analyze consumer discussions in the [INDUSTRY/CATEGORY] space over the past 30 days. Identify emerging trends, shifting preferences, unmet needs, and gaps in current product offerings. Focus on what consumers wish existed but can't find."*

3. **Discovery-Focused Agent Work**
   - **Insight Agent**: Identifies rising topics and declining topics in database
   - **Media Agent**: Analyzes consumer-generated content trends (DIY solutions, hacks)
   - **Query Agent**: Tracks emerging startups and innovative products getting attention
   - **Forum Engine**: Agents debate which trends are fads vs. lasting shifts

4. **Market Intelligence Report**
   - Report sections:
     - **Trend Velocity Rankings**: Which topics are growing fastest
     - **Consumer Language Evolution**: New terminology and framing
     - **Unmet Needs Analysis**: "I wish" and "why doesn't anyone make" patterns
     - **Cross-Category Inspiration**: Trends spreading from other industries
     - **Demographic Segments**: Different preferences by age/region/lifestyle
     - **Innovation Opportunities**: White space for new products/features

5. **Validate Findings with Deeper Research**
   - Query: *"Deep dive into [SPECIFIC_TREND]. Who is discussing it? What specific features do they want? How much would they pay? What alternatives are they currently using?"*

6. **Create Trend Watch Dashboard**
   - Set up recurring monthly market scans
   - Track keyword emergence and growth rates
   - Monitor competitive responses to trends

**Advanced Applications**:
- A/B test product concepts by analyzing similar existing product discussions
- Identify early adopter communities for beta testing
- Predict category disruption signals (dissatisfaction patterns)

---

## Use Case 8: Crisis Scenario Planning & Simulation

**Goal**: Prepare for potential PR crises by analyzing similar past events

### Step-by-Step Process

1. **Historical Crisis Data Collection**
   ```bash
   cd MindSpider
   # Collect data from previous crisis periods (yours or competitors)
   python main.py --complete --date 2023-06-15  # Known crisis date
   ```

2. **Submit Crisis Analysis Query**
   - Query: *"Analyze the public opinion crisis that [COMPANY] faced regarding [ISSUE] in [TIMEFRAME]. Document the timeline of sentiment deterioration, identify key influencers who amplified the crisis, assess effectiveness of company responses, and extract lessons for crisis prevention and management."*

3. **Crisis Anatomy Analysis**
   - **Insight Agent**: Identifies crisis triggers and escalation patterns
   - **Media Agent**: Analyzes how visual content spread the crisis
   - **Query Agent**: Tracks mainstream media pickup and amplification
   - **Forum Engine**: Agents debate whether crisis was preventable

4. **Crisis Playbook Development**
   - Report sections:
     - **Crisis Lifecycle**: Trigger → Escalation → Peak → Resolution phases
     - **Sentiment Cascade Analysis**: How negative sentiment spread
     - **Response Effectiveness**: What worked vs. what backfired
     - **Key Influencer Roles**: Who amplified, who defended
     - **Recovery Timeline**: How long until sentiment normalized
     - **Preventive Indicators**: Early warning signs to monitor

5. **Create Crisis Response Templates**
   - Develop response strategies for different crisis types
   - Identify spokesperson requirements and messaging guidelines
   - Create escalation protocols based on sentiment thresholds

6. **Run Crisis Simulations**
   - Query: *"If we faced a similar crisis today about [HYPOTHETICAL_ISSUE], predict how it would unfold based on current brand sentiment and our audience composition. What would be the likely severity and recovery time?"*

**Practical Applications**:
- Train PR team with real crisis examples
- Develop crisis communication playbooks
- Set up automated crisis detection systems
- Conduct quarterly crisis preparedness reviews

---

## General Tips for All Use Cases

### Optimizing Query Formulation

**Bad Query**: "Analyze my brand"
**Good Query**: "Analyze sentiment about [BRAND_NAME] on Weibo, Xiaohongshu, and Douyin over the past 7 days. Focus on product quality mentions, customer service experiences, and comparison with [COMPETITOR]. Identify top 3 issues requiring immediate attention."

**Key Elements of Effective Queries**:
1. Specific topic/brand names
2. Time frame
3. Platform focus (if relevant)
4. Specific aspects to analyze
5. Desired output format/priorities

### Leveraging the Forum Engine

The Forum Engine's agent debate often surfaces insights that individual agents miss. Pay special attention to:
- Points of disagreement between agents (indicates ambiguous signals)
- Unanimous agent concerns (high-confidence findings)
- Moderator summaries (synthesized key insights)

Review `logs/forum.log` for the full debate:
```bash
tail -f logs/forum.log  # Monitor real-time
```

### Custom Business Data Integration

For deeper insights, integrate your private business data:

1. **Sales Data**: Correlate sentiment with sales performance
2. **Support Tickets**: Link social complaints to internal issues
3. **Product Telemetry**: Connect user behavior data with feedback
4. **CRM Data**: Segment analysis by customer value

Example integration:
```python
# In InsightEngine/tools/custom_business_tool.py
class SalesCorrelationTool:
    def analyze_sentiment_vs_sales(self, date_range):
        # Query sentiment from MindSpider database
        sentiment_data = self.get_sentiment_scores(date_range)

        # Query sales from your business database
        sales_data = self.get_sales_data(date_range)

        # Calculate correlation
        correlation = self.correlate(sentiment_data, sales_data)
        return correlation
```

### Report Customization

Create custom report templates for recurring use cases:

1. Create template in `ReportEngine/report_template/brand_crisis_template.md`
2. Use clear section headers
3. Include placeholders for data visualization
4. Report Agent will automatically select appropriate template

### Performance Optimization for Large-Scale Analysis

For analyzing millions of data points:

1. **Use Database Indexing**:
   ```sql
   CREATE INDEX idx_sentiment_date ON sentiment_data(created_date, sentiment);
   CREATE INDEX idx_topic ON sentiment_data(topic);
   ```

2. **Batch Processing**:
   ```bash
   # Process data in weekly chunks
   for date in 2024-01-01 2024-01-08 2024-01-15; do
       python main.py --complete --date $date
   done
   ```

3. **GPU Acceleration for Sentiment Analysis**:
   ```bash
   pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
   ```

### Scheduling Automated Analysis

Set up cron jobs for recurring analysis:

```bash
# Edit crontab
crontab -e

# Daily crawler at 2 AM
0 2 * * * cd /path/to/BettaFish/MindSpider && python main.py --complete --date $(date +\%Y-\%m-\%d)

# Weekly competitive intelligence report (Mondays at 9 AM)
0 9 * * 1 cd /path/to/BettaFish && python scripts/weekly_competitive_report.py

# Hourly crisis monitoring during active campaigns
0 * * * * cd /path/to/BettaFish && python scripts/crisis_monitor.py
```

---

## ROI Measurement Framework

To demonstrate value of the platform, track these metrics:

### Crisis Prevention
- **Metric**: Hours of early warning before crisis peaks
- **Value**: Cost of crisis * probability of prevention

### Product Development
- **Metric**: Number of validated feature requests from social listening
- **Value**: Cost savings from avoiding failed features

### Marketing Optimization
- **Metric**: Improvement in influencer campaign ROI
- **Value**: Marketing spend × efficiency improvement %

### Competitive Advantage
- **Metric**: Days ahead of competitors in trend identification
- **Value**: First-mover advantage in market positioning

### Customer Satisfaction
- **Metric**: Reduction in complaint frequency after addressing pain points
- **Value**: Reduced support costs + improved retention

---

## Next Steps

1. **Choose Your Primary Use Case**: Start with the most critical business need
2. **Configure System**: Set up crawler and agents with appropriate API keys
3. **Collect Baseline Data**: Run crawler for 7-30 days to build database
4. **Run First Analysis**: Submit your first query and review the report
5. **Iterate and Refine**: Adjust queries and configurations based on results
6. **Scale Up**: Add more use cases and automate recurring analyses
7. **Integrate Insights**: Feed findings into business decision-making processes

For additional support, refer to:
- `CLAUDE.md` - Technical architecture and development guide
- `README.md` - Installation and quick start
- `config.py` - Configuration options reference

---

**Questions or Issues?**
Review the troubleshooting section in `CLAUDE.md` or check agent logs in `logs/` directory for detailed execution information.

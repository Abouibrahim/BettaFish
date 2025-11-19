# API Setup Guide for BettaFish (English Content)

This guide provides step-by-step instructions for obtaining all required API keys for running BettaFish with English content and international platforms.

## Overview

BettaFish requires API keys for:
- **LLM Providers**: Power the intelligent agents
- **Search APIs**: Enable web search capabilities

## Required LLM API Keys

### 1. OpenAI API Key (GPT-4o / GPT-3.5-turbo)

**Used for**: Insight Agent, Report Agent, Forum Host, Query Agent

**Step-by-step:**

1. **Create an OpenAI Account**
   - Go to https://platform.openai.com/signup
   - Sign up with email or Google/Microsoft account
   - Verify your email address

2. **Add Payment Method**
   - Go to https://platform.openai.com/account/billing/overview
   - Click "Add payment method"
   - Add a credit/debit card (required for API access)
   - Consider setting usage limits to control costs

3. **Generate API Key**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name it (e.g., "BettaFish Production")
   - Copy the key immediately (you won't see it again!)
   - Save it securely

4. **Configuration**
   ```env
   # For Insight Agent
   INSIGHT_ENGINE_API_KEY=sk-proj-xxxxxxxxxxxxx
   INSIGHT_ENGINE_BASE_URL=https://api.openai.com/v1
   INSIGHT_ENGINE_MODEL_NAME=gpt-4o

   # For Report Agent
   REPORT_ENGINE_API_KEY=sk-proj-xxxxxxxxxxxxx
   REPORT_ENGINE_BASE_URL=https://api.openai.com/v1
   REPORT_ENGINE_MODEL_NAME=gpt-4o

   # For Forum Host
   FORUM_HOST_API_KEY=sk-proj-xxxxxxxxxxxxx
   FORUM_HOST_BASE_URL=https://api.openai.com/v1
   FORUM_HOST_MODEL_NAME=gpt-4o

   # For Query Agent (use cheaper model)
   QUERY_ENGINE_API_KEY=sk-proj-xxxxxxxxxxxxx
   QUERY_ENGINE_BASE_URL=https://api.openai.com/v1
   QUERY_ENGINE_MODEL_NAME=gpt-3.5-turbo
   ```

**Cost Estimate:**
- GPT-4o: $2.50 per 1M input tokens, $10.00 per 1M output tokens
- GPT-3.5-turbo: $0.50 per 1M input tokens, $1.50 per 1M output tokens

**Tips:**
- You can use the same API key for all agents
- Set usage limits at https://platform.openai.com/account/limits
- Monitor usage at https://platform.openai.com/usage

---

### 2. Google Gemini API Key (Gemini 2.5 Pro)

**Used for**: Media Agent (multimodal content analysis)

**Step-by-step:**

1. **Get a Google Cloud Account**
   - Go to https://ai.google.dev/gemini-api/docs/api-key
   - Click "Get an API key"
   - Sign in with your Google account

2. **Create API Key**
   - Click "Create API key"
   - Select "Create API key in new project" or use existing project
   - Copy the generated API key
   - Save it securely

3. **Enable Gemini API**
   - The API should be automatically enabled
   - If not, go to Google Cloud Console
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gemini API" and enable it

4. **Configuration**
   ```env
   MEDIA_ENGINE_API_KEY=AIzaSyxxxxxxxxxxxxx
   MEDIA_ENGINE_BASE_URL=https://generativelanguage.googleapis.com/v1beta
   MEDIA_ENGINE_MODEL_NAME=gemini-2.0-flash-exp
   ```

**Cost Estimate:**
- Gemini 2.0 Flash: Free tier available (15 requests per minute)
- After free tier: $0.075 per 1M input tokens, $0.30 per 1M output tokens

**Tips:**
- Gemini has excellent multimodal capabilities for image/video analysis
- Free tier is generous for testing
- Rate limits: 15 RPM (requests per minute) on free tier

---

### 3. Anthropic Claude API Key (Alternative)

**Used for**: Can replace OpenAI for any agent

**Step-by-step:**

1. **Create Anthropic Account**
   - Go to https://console.anthropic.com/
   - Click "Sign up"
   - Verify your email

2. **Add Credits**
   - Go to https://console.anthropic.com/settings/billing
   - Add payment method
   - Purchase credits ($5 minimum)

3. **Generate API Key**
   - Go to https://console.anthropic.com/settings/keys
   - Click "Create key"
   - Name it (e.g., "BettaFish")
   - Copy and save the key

4. **Configuration**
   ```env
   # Example: Using Claude for Insight Agent
   INSIGHT_ENGINE_API_KEY=sk-ant-xxxxxxxxxxxxx
   INSIGHT_ENGINE_BASE_URL=https://api.anthropic.com/v1
   INSIGHT_ENGINE_MODEL_NAME=claude-3-5-sonnet-20241022
   ```

**Cost Estimate:**
- Claude 3.5 Sonnet: $3.00 per 1M input tokens, $15.00 per 1M output tokens
- Claude 3.5 Haiku: $0.80 per 1M input tokens, $4.00 per 1M output tokens

**Tips:**
- Claude is excellent for analytical reasoning
- Good alternative to OpenAI for privacy-conscious users
- Supports longer context windows (200K tokens)

---

## Required Search API Keys

### 4. Tavily Search API Key

**Used for**: Web search in Query Agent

**Step-by-step:**

1. **Create Tavily Account**
   - Go to https://tavily.com/
   - Click "Get Started" or "Sign Up"
   - Sign up with email or Google account

2. **Verify Email**
   - Check your email for verification link
   - Click the link to verify your account

3. **Get API Key**
   - Log in to https://app.tavily.com/
   - Navigate to "API Keys" section
   - Your API key should be displayed
   - Copy the API key

4. **Configuration**
   ```env
   TAVILY_API_KEY=tvly-xxxxxxxxxxxxx
   ```

**Cost Estimate:**
- Free tier: 1,000 searches per month
- Pro: $49/month for 10,000 searches
- Enterprise: Custom pricing

**Tips:**
- Free tier is sufficient for testing and small deployments
- Tavily specializes in AI-optimized search results
- Returns structured data perfect for LLM consumption

---

### 5. Bocha AI Search API Key (Optional)

**Used for**: Multimodal search capabilities

**Step-by-step:**

1. **Create Bocha Account**
   - Go to https://open.bochaai.com/
   - Click "Register" or "Sign Up"
   - Complete registration form

2. **Verify Account**
   - Verify your email address
   - Log in to the dashboard

3. **Create API Key**
   - Navigate to "API Keys" section
   - Click "Create New API Key"
   - Select "AI Search" service
   - Copy the API key

4. **Configuration**
   ```env
   BOCHA_BASE_URL=https://api.bochaai.com/v1/ai-search
   BOCHA_WEB_SEARCH_API_KEY=bch-xxxxxxxxxxxxx
   ```

**Cost Estimate:**
- Check current pricing at https://open.bochaai.com/pricing
- Usually offers free trial credits

**Tips:**
- Bocha is optional but adds multimodal search capabilities
- Useful for searching images and videos
- Can be skipped if budget is constrained

---

## Recommended Configuration for English Content

### Budget-Friendly Setup (Minimum Cost)

```env
# Use GPT-3.5-turbo for everything (cheapest)
INSIGHT_ENGINE_API_KEY=your_openai_key
INSIGHT_ENGINE_BASE_URL=https://api.openai.com/v1
INSIGHT_ENGINE_MODEL_NAME=gpt-3.5-turbo

MEDIA_ENGINE_API_KEY=your_gemini_key
MEDIA_ENGINE_BASE_URL=https://generativelanguage.googleapis.com/v1beta
MEDIA_ENGINE_MODEL_NAME=gemini-2.0-flash-exp

QUERY_ENGINE_API_KEY=your_openai_key
QUERY_ENGINE_BASE_URL=https://api.openai.com/v1
QUERY_ENGINE_MODEL_NAME=gpt-3.5-turbo

REPORT_ENGINE_API_KEY=your_openai_key
REPORT_ENGINE_BASE_URL=https://api.openai.com/v1
REPORT_ENGINE_MODEL_NAME=gpt-3.5-turbo

FORUM_HOST_API_KEY=your_openai_key
FORUM_HOST_BASE_URL=https://api.openai.com/v1
FORUM_HOST_MODEL_NAME=gpt-3.5-turbo

TAVILY_API_KEY=your_tavily_key
```

**Estimated monthly cost**: $10-50 depending on usage

---

### Balanced Setup (Recommended)

```env
# Use GPT-4o for critical agents, GPT-3.5 for simple tasks
INSIGHT_ENGINE_API_KEY=your_openai_key
INSIGHT_ENGINE_BASE_URL=https://api.openai.com/v1
INSIGHT_ENGINE_MODEL_NAME=gpt-4o

MEDIA_ENGINE_API_KEY=your_gemini_key
MEDIA_ENGINE_BASE_URL=https://generativelanguage.googleapis.com/v1beta
MEDIA_ENGINE_MODEL_NAME=gemini-2.0-flash-exp

QUERY_ENGINE_API_KEY=your_openai_key
QUERY_ENGINE_BASE_URL=https://api.openai.com/v1
QUERY_ENGINE_MODEL_NAME=gpt-3.5-turbo

REPORT_ENGINE_API_KEY=your_openai_key
REPORT_ENGINE_BASE_URL=https://api.openai.com/v1
REPORT_ENGINE_MODEL_NAME=gpt-4o

FORUM_HOST_API_KEY=your_openai_key
FORUM_HOST_BASE_URL=https://api.openai.com/v1
FORUM_HOST_MODEL_NAME=gpt-4o

TAVILY_API_KEY=your_tavily_key
```

**Estimated monthly cost**: $50-200 depending on usage

---

### Premium Setup (Best Quality)

```env
# Use GPT-4o everywhere for maximum quality
INSIGHT_ENGINE_API_KEY=your_openai_key
INSIGHT_ENGINE_BASE_URL=https://api.openai.com/v1
INSIGHT_ENGINE_MODEL_NAME=gpt-4o

MEDIA_ENGINE_API_KEY=your_gemini_key
MEDIA_ENGINE_BASE_URL=https://generativelanguage.googleapis.com/v1beta
MEDIA_ENGINE_MODEL_NAME=gemini-2.0-flash-exp

QUERY_ENGINE_API_KEY=your_openai_key
QUERY_ENGINE_BASE_URL=https://api.openai.com/v1
QUERY_ENGINE_MODEL_NAME=gpt-4o

REPORT_ENGINE_API_KEY=your_openai_key
REPORT_ENGINE_BASE_URL=https://api.openai.com/v1
REPORT_ENGINE_MODEL_NAME=gpt-4o

FORUM_HOST_API_KEY=your_openai_key
FORUM_HOST_BASE_URL=https://api.openai.com/v1
FORUM_HOST_MODEL_NAME=gpt-4o

TAVILY_API_KEY=your_tavily_key
BOCHA_BASE_URL=https://api.bochaai.com/v1/ai-search
BOCHA_WEB_SEARCH_API_KEY=your_bocha_key
```

**Estimated monthly cost**: $200-500 depending on usage

---

## Testing Your API Keys

After setting up your API keys, test them:

```bash
# Test OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_OPENAI_API_KEY"

# Test Gemini
curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_GEMINI_KEY"

# Test Tavily
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{"api_key": "YOUR_TAVILY_KEY", "query": "test"}'
```

---

## Security Best Practices

1. **Never commit API keys to version control**
   - Always use `.env` file (which is in `.gitignore`)
   - Never hardcode keys in source code

2. **Use environment-specific keys**
   - Separate keys for development, staging, and production
   - Rotate keys periodically

3. **Set usage limits**
   - OpenAI: https://platform.openai.com/account/limits
   - Monitor usage regularly to avoid unexpected charges

4. **Store keys securely**
   - Use password managers or secret management tools
   - Never share keys via email or chat

---

## Troubleshooting

### "Invalid API Key" Error
- Check that you copied the entire key correctly
- Ensure no extra spaces or newlines
- Verify the key hasn't been revoked
- Check that billing is active (for OpenAI)

### "Rate Limit Exceeded" Error
- You've hit the API provider's rate limits
- Wait a few minutes and try again
- Upgrade to a higher tier plan
- Implement request throttling in your code

### "Insufficient Credits" Error
- Add credits to your account
- Check billing settings
- Verify payment method is valid

### Connection Errors
- Check your internet connection
- Verify the BASE_URL is correct
- Check if the API provider has an outage (status pages)

---

## Cost Optimization Tips

1. **Use appropriate models for each task**
   - Use GPT-3.5-turbo for simple tasks
   - Reserve GPT-4o for complex analysis

2. **Implement caching**
   - Cache frequently asked queries
   - Avoid redundant API calls

3. **Set token limits**
   - Limit max tokens in responses
   - Truncate long inputs when possible

4. **Monitor usage**
   - Check usage dashboards weekly
   - Set up billing alerts

5. **Use free tiers wisely**
   - Gemini offers generous free tier
   - Tavily free tier good for testing

---

## Support and Resources

- **OpenAI Documentation**: https://platform.openai.com/docs
- **Gemini Documentation**: https://ai.google.dev/docs
- **Claude Documentation**: https://docs.anthropic.com
- **Tavily Documentation**: https://docs.tavily.com
- **BettaFish Issues**: https://github.com/your-repo/issues

---

## Next Steps

After obtaining all API keys:

1. Copy `.env.example` to `.env`
2. Fill in your API keys in `.env`
3. Run `python app.py` to start the system
4. Access the web interface at http://localhost:5000
5. Test with a simple query to verify everything works

Good luck with your BettaFish deployment!

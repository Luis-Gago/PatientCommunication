# PaCo Deployment Costs

Complete cost breakdown for running PaCo in production.

## Monthly Infrastructure Costs

| Service | Purpose | Free Tier | Paid Plan | Recommended |
|---------|---------|-----------|-----------|-------------|
| **Neon** | PostgreSQL Database | ✅ 512 MB storage | $19/mo (10 GB) | **Free Tier** |
| **Railway** | Backend API | ❌ None | ~$5-10/mo usage-based | **Paid** (~$5-10) |
| **Vercel** | Frontend Hosting | ✅ 100 GB bandwidth | $20/mo (Pro) | **Free Tier** |

### API Service Costs (Variable)

| Service | Purpose | Cost Model | Est. Monthly |
|---------|---------|------------|--------------|
| **ElevenLabs** | Voice AI | Per character or subscription | $5-22/mo |
| **Groq** | Medication Analysis (LLM) | FREE with rate limits | $0/mo |

## Total Monthly Cost Estimate

### Minimal Setup (Perfect for Research/Academic)
- **Neon Database**: $0 (Free)
- **Railway Backend**: $5-10
- **Vercel Frontend**: $0 (Free)
- **ElevenLabs**: $5 (Starter)
- **Groq AI**: $0 (Free with limits)
- **Total: ~$10-15/month** ✅

### Typical Production Setup
- **Neon Database**: $0-19 (Free or Scale)
- **Railway Backend**: $10-20
- **Vercel Frontend**: $0-20 (Free or Pro)
- **ElevenLabs**: $22 (Creator)
- **Groq AI**: $0 (Free with limits)
- **Total: ~$32-61/month**

## Service Details

### Neon PostgreSQL (FREE! ⭐)

**Free Tier Includes:**
- ✅ 512 MB storage
- ✅ Unlimited databases
- ✅ Instant branching (dev/staging/prod)
- ✅ Point-in-time restore (7 days)
- ✅ Auto-suspend (saves resources)
- ✅ Enough for 50,000+ conversation messages

**When to Upgrade:**
- Storage > 512 MB
- Need more compute
- Longer restore window (30 days)

**Paid Plans:**
- $19/mo: 10 GB storage, more compute
- $69/mo: 50 GB storage, dedicated resources

**Perfect for:**
- ✅ Research projects
- ✅ Academic studies
- ✅ Pilot programs
- ✅ Low-traffic applications

### Railway Backend

**Pricing:**
- Usage-based (no free tier since Aug 2023)
- $0.000231/GB-hour (RAM)
- $0.000463/vCPU-hour (CPU)
- Minimum ~$5/month for basic backend

**Estimated Costs:**
- Low traffic: $5-10/month
- Medium traffic: $10-20/month
- High traffic: $20-50/month

**What You Get:**
- ✅ Auto-deployments from GitHub
- ✅ Auto-scaling
- ✅ Built-in monitoring
- ✅ Easy environment variables
- ✅ CLI tools

### Vercel Frontend (FREE! ⭐)

**Free Tier Includes:**
- ✅ 100 GB bandwidth/month
- ✅ Unlimited deployments
- ✅ Auto-scaling
- ✅ Global CDN
- ✅ SSL certificates
- ✅ Perfect for research projects

**When to Upgrade:**
- Bandwidth > 100 GB/month
- Need analytics
- Custom domains with advanced features

**Paid Plans:**
- $20/mo: 1 TB bandwidth, analytics

**Perfect for:**
- ✅ Research projects (easily under 100 GB)
- ✅ Academic studies
- ✅ Pilot programs

### ElevenLabs Voice AI

**Pricing:**
- **Free**: 10,000 characters/month
- **Starter** ($5/mo): 30,000 characters/month
- **Creator** ($22/mo): 100,000 characters/month
- **Pro** ($99/mo): 500,000 characters/month

**Estimation:**
- Average conversation: ~500-1000 characters
- Starter plan: ~30-60 conversations/month
- Creator plan: ~100-200 conversations/month

**Recommendation:**
- Start with **Starter ($5/mo)** for pilot
- Upgrade to **Creator ($22/mo)** for active research

### Groq AI (Medication Analysis) - FREE! ⭐

**Pricing:**
- FREE tier with generous rate limits
- Llama 3.3 70B: FREE
- Mixtral models: FREE

**Rate Limits (Free Tier):**
- 30 requests/minute
- 14,400 requests/day
- More than enough for medication analysis

**Medication Analysis Costs:**
- Per analysis: $0 (FREE!)
- Unlimited analyses within rate limits
- Perfect for research projects with budgets

**Recommendation:**
- Use the FREE tier (perfect for research)
- No need to upgrade for typical research usage

## Cost Optimization Tips

### 1. Use Free Tiers Maximally
- ✅ Neon Database (Free forever)
- ✅ Vercel Frontend (Free for hobby)
- ✅ Only pay for Railway backend (~$5-10)

### 2. Optimize Database Usage
- Use Neon's auto-suspend feature
- Archive old conversations periodically
- Use database branching instead of multiple instances

### 3. Optimize API Calls
- Groq AI is FREE - analyze as much as needed!
- ElevenLabs: Batch analyze conversations instead of real-time
- Use shorter system prompts when possible

### 4. Monitor Usage
- Set up billing alerts in Railway
- Track ElevenLabs character usage
- Monitor Groq rate limits (though generous)

### 5. Scale Gradually
- Start with minimal setup (~$10-15/month)
- Only upgrade when you hit limits
- Monitor actual usage before upgrading

## Academic/Research Pricing

### Grant Budget Considerations

**Annual Costs:**
- Minimal: ~$120-180/year
- Typical: ~$400-700/year

**Cost per Research Participant:**
- Backend: ~$0.10-0.20/participant/month
- Database: $0 (free)
- Voice AI: ~$0.50-1.00/conversation
- Analysis: $0 (Groq is free!)

**For 100 Participants:**
- Infrastructure: ~$10-20/month
- Voice conversations: ~$50-100/month (2 convos/participant)
- Medication analysis: ~$10-50/month
- **Total: ~$70-170/month** or **$840-2040/year**

## Alternative: Fully Free Development Setup

For development/testing only:

- **Database**: Neon Free Tier ($0)
- **Backend**: Run locally or use Railway trial ($0-5)
- **Frontend**: Vercel Free Tier ($0)
- **ElevenLabs**: Free tier with 10k chars ($0)
- **OpenAI**: Free trial credits ($0)

**Total: $0-5/month** for development! 🎉

## Comparison with Other Solutions

| Solution | Monthly Cost | Database | Backend | Frontend |
|----------|--------------|----------|---------|----------|
| **PaCo (Our Setup)** | **$12-20** | Neon Free | Railway $5-10 | Vercel Free |
| All Railway | $25-40 | Railway $10-15 | Railway $10-20 | Railway $5 |
| AWS EC2 | $30-50+ | RDS $15-30 | EC2 $10-20 | S3+CF $5 |
| Heroku | $32+ | Heroku $9 | Heroku $7 | Heroku $7+ |
| DigitalOcean | $24+ | Droplet $12 | Droplet $12 | CDN included |

**Our setup is the most cost-effective!** ✅

## Conclusion

### Best Setup for Research Projects:

1. **Neon PostgreSQL**: FREE (512 MB is plenty)
2. **Railway Backend**: ~$5-10/month
3. **Vercel Frontend**: FREE (100 GB bandwidth)
4. **ElevenLabs**: $5-22/month depending on usage
5. **OpenAI**: $5-20/month depending on analysis frequency

**Total: $15-52/month** - Extremely affordable for a complete healthcare research platform!

### Scaling Path:

1. **Pilot (10-20 participants)**: $15-30/month
2. **Active Research (50-100 participants)**: $50-100/month
3. **Large Study (200+ participants)**: $100-200/month

All costs scale with actual usage - no waste! 🎯

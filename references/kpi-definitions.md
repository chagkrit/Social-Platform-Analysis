# KPI Definitions

Use consistent formulas before comparing platforms. Do not compare raw engagement counts without denominators.

## Recommended CSV Columns

Minimum useful columns:

- `platform`
- `period`
- `posts`
- `followers_start`
- `followers_end`
- `reach`
- `impressions`
- `likes`
- `comments`
- `shares`
- `saves`
- `clicks`
- `video_views`
- `earned_mentions`
- `earned_reach`

Optional columns:

- `paid_reach`
- `organic_reach`
- `campaign_name`
- `content_pillar`
- `crisis_or_event_flag`

## Core Formulas

- Total engagement = likes + comments + shares + saves + clicks.
- Engagement rate by reach = total engagement / reach.
- Engagement rate by followers = total engagement / followers_end.
- Amplification rate = shares / reach.
- Save/share quality ratio = (saves + shares) / total engagement.
- Comment depth ratio = comments / total engagement.
- Follower growth rate = (followers_end - followers_start) / followers_start.
- Posting consistency = posts per period, interpreted against institutional capacity.
- Reach power = reach or impressions, but label the denominator used.
- Earned amplification ratio = earned_reach / reach.
- Earned mention rate = earned_mentions / posts.

## Denominator Rules

- Prefer reach over followers for content efficiency when reach is available.
- Use followers only when reach is unavailable and label confidence lower.
- Do not mix impressions and reach without labeling.
- Do not combine paid and organic performance unless paid/organic split is unavailable and explicitly noted.
- For video-first platforms, report views separately from engagement.

## Data Limitation Flags

Flag:

- Missing reach or impressions.
- Missing paid/organic split.
- Different reporting periods across platforms.
- Campaign spikes or crisis events.
- Competitor data from non-equivalent sources.
- No earned-media data.
- Small post count that makes rates unstable.

## Benchmark Fairness

Normalize by:

- Per reach.
- Per follower.
- Per post.
- Per content pillar.
- Per campaign period.

Compare organizations by type when possible: teaching hospital vs private hospital vs medical faculty vs public-health agency.

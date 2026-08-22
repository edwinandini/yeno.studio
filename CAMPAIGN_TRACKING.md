# Campaign tracking

Google Analytics can only assign a source when the visit carries referral or campaign information. Links opened from messaging apps, copied URLs, email clients, PDFs, and some privacy tools often arrive without a referrer and are therefore reported as direct.

Use a complete, consistent UTM set on every link placed outside the site:

```text
https://yeno.studio/journal/example/?utm_source=linkedin&utm_medium=organic_social&utm_campaign=daily_journal&utm_content=example
```

## Naming convention

- `utm_source`: the platform or partner, in lowercase (`linkedin`, `instagram`, `whatsapp`, `newsletter`, `partner_name`).
- `utm_medium`: the channel (`organic_social`, `paid_social`, `email`, `messaging`, `referral`, `cpc`).
- `utm_campaign`: the stable initiative name (`daily_journal`, `product_launch_q3`).
- `utm_content`: the post slug, creative variant, or placement.
- Add `utm_id` when a campaign has a stable ID in another system.

Do not add UTMs to internal links on yeno.studio. Keep parameter names and values lowercase, and use the same spelling across every placement. Preserve Google Ads auto-tagging; do not remove `gclid` values in redirects.

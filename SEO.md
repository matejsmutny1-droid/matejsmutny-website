# SEO and Google indexing

The canonical website is https://matejsmutny.com/. The home page represents Matej Smutný (also known as Matej Smutny); individual pages represent music, albums and merchandise.

## Included

- Unique page titles and descriptions, canonical URLs, social preview metadata.
- WebSite and Person JSON-LD on the home page, WebPage data throughout, MusicRecording data on audio pages. These describe the content; they do not guarantee a Google rich result.
- Crawl discovery through `/robots.txt` and `/sitemap.xml` (32 canonical content pages).
- Privacy and order-confirmation pages use `noindex, follow` and stay out of the sitemap. They remain accessible.
- Lightweight home-page image, lazy loading for cover art, and deferred audio loading.

Run `python3 scripts/check_seo.py` after adding or changing pages. Add a new indexable page to the sitemap. Do not invent publication dates or update sitemap lastmod dates when content has not changed.

## Google Search Console: account step still required

1. Sign in at https://search.google.com/search-console/ with the site owner's Google account.
2. Select the existing property, or add the URL-prefix property `https://matejsmutny.com/`.
3. If verification is required, choose HTML tag and copy Google's exact `google-site-verification` meta tag. Add that tag to the head of index.html, deploy it, then select Verify in Search Console. Preserve any existing verification token. Alternatively, verify a Domain property using the DNS record supplied by Google.
4. In Sitemaps, submit `https://matejsmutny.com/sitemap.xml`.
5. Inspect `https://matejsmutny.com/` using URL Inspection, run Test Live URL, then Request Indexing if appropriate.
6. Review Page Indexing for exclusions and Performance for queries such as `matej smutny` and `matej smutný`. A public search or an HTTP 200 response alone cannot confirm Google's index state.

Search Console ownership and submission have not been completed by code deployment alone. Crawling and ranking are controlled by Google and can take time.

## Ongoing work

Keep concert information current. Ensure public artist profiles and promoter pages link to the canonical website where their editors allow it. Maintain one consistent artist identity and useful original content. Avoid hidden keywords, duplicate language pages without translations, paid spam links and promises of guaranteed first place.

Official guidance:
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl
- https://support.google.com/webmasters/answer/9008080

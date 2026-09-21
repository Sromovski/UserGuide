# Public cover images

These exist because **Gumroad's cover endpoint requires a PUBLIC image URL** and rejects
the S3 url its own presign flow returns. Every other product solves this by pulling
`url_fullxfull` from its matching Etsy listing — see `gumroadpub.publish.etsy_cover_urls`.

`12-start-here` cannot: it is the free lead magnet, and **Etsy has no free listing tier**,
so it has no Etsy listing to pull images from. Without these files it appears in the
Gumroad store as a blank tile — the worst possible state for the one product whose whole
job is to pull people in.

They are served from `raw.githubusercontent.com`, so **this only works while the repo is
public.** If `Sromovski/UserGuide` is ever made private, these URLs stop resolving and the
Start Here cover disappears from Gumroad. Re-host them somewhere public and update
`gumroadpub.publish.PUBLIC_COVERS` if that happens.

Regenerate with:

    python -c "from covers import catalogue, render; s=catalogue.all_specs()['12-start-here']; render.render(s,'wide').save(r'assets\covers\start-here-wide.png', optimize=True); render.render(s,'square').save(r'assets\covers\start-here-square.png', optimize=True)"

Landscape goes first — Gumroad's storefront grid is landscape and makes the first cover
the thumbnail.

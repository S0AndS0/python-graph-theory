---
layout: page
title: About
permalink: /about/
---

## ... this site

At it's core this site's documentation is built in large part thanks to the [Jekyll][jekyll-docs] teams' amazing work both with their projects and with fostering an astounding level of team-work within the community of Open Source developers. Other third party resources utilized in building this site are (but probably not limited to) the following unordered list.


> Note; if you believe you have contributed, or that your content or code has been used without citation, the fastest and easiest route is to [fork this repo][this-repo] and correct it with a `pull request` (see GitHub's [About pull requests][about-pull-requests] for general tips), second fastest would be to [Open an Issue][got-issues] to notify project maintainers of the error.


- [Minima][theme] _"is a one-size-fits-all Jekyll theme for writers."_
- [MathJax][mathjax] _"is an open-source JavaScript display engine for LaTeX, MathML, and AsciiMath notation that works in all modern browsers."_
- [Liquid][liquid] _"is a template engine which was written with very specific requirements"..._


## ... contributers


- [Raven Cheuk](https://math.stackexchange.com/users/647646/raven-cheuk) who asked a [question](https://math.stackexchange.com/questions/3130866/modelling-congestion-games-in-python-without-tons-of-for-loop) only to find so many more ways to _interrogate_ a problem for [answers][points-posts].


{% comment %}
Note to Raven Cheuk, feel free to edit that above when you've the chance and desire to do so.
{% endcomment %}


## ... privacy


Seems like every site has to address this somewhere these days, _quick-n-short of it_ is The project maintainers at this point are __not__ interested in collecting or storing such things. GitHub and CDNs utilized to bring you this site are the only entities (that project maintainers are aware of) at all concerned with directly collecting your meta-data here.


[jekyll-docs]: https://jekyllrb.com/docs/home
[this-repo]: https://github.com/S0AndS0/python-graph-theory/
[got-issues]: https://github.com/S0AndS0/python-graph-theory/issues/
[theme]: https://github.com/jekyll/minima
[mathjax]: https://docs.mathjax.org/en/latest/start.html
[liquid]: https://github.com/Shopify/liquid
[about-pull-requests]: https://help.github.com/en/articles/about-pull-requests

{% capture points_posts %}{%- post_url 2019-04-02-points-00-preface -%}{% endcapture %}
[points-posts]: {{ points_posts | relative_url }}

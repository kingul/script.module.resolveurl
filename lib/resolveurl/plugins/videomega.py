"""
    Kodi resolveurl plugin
    Copyright (C) 2019
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError


class VideoMegaResolver(ResolveUrl):
    name = "videomega"
    domains = ["videomega.co"]
    pattern = r'(?://|\.)(videomega\.co)/(?:f|e)/(\w+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        response = self.net.http_GET(web_url, headers=headers)
        response_headers = response.get_headers(as_dict=True)
        cookies = response_headers.get('Set-Cookie')
        cookie = ''
        for ck in cookies.split('Only, '):
            cookie += ck.split(';')[0] + '; '
        headers.update({'Cookie': cookie[:-2],
                        'Referer': web_url})
        html = self.net.http_GET('https://{}/js/{}'.format(host, media_id), headers=headers).content
        sources = helpers.scrape_sources(html)
        if sources:
            return helpers.pick_source(sources) + helpers.append_headers(headers)
        raise ResolverError("Video not found")


    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/e/{media_id}')

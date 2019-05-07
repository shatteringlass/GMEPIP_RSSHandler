import requests
import xmltodict

from .db import orm
from .models import Outage

from lxml import etree
from loguru import logger



class GMEPIPRssHandler:

    gme_feed_url = "https://pip.ipex.it/PipWa/Front/GetAcerFeedsPower"
    xpt = "/rss/channel/item/description"

    def __init__(self):
        _xml = etree.fromstring(requests.get(self.gme_feed_url).content)
        self._msgs = _xml.xpath(self.xpt)

    @property
    def msgs(self):
        return self._msgs

    @orm.db_session
    def to_db(self):
        logger.info(f"Read data from GME PIP RSS, attempting database upload for {len(self.msgs)} items.")
        for msg in self.msgs:
            j = xmltodict.parse(msg.text)[
                'ns1:REMITUrgentMarketMessages']['ns1:UMM']
            p = Outage.loads(j)
            Outage.get_or_create(p)
        logger.info("Database upload completed.")

from datetime import datetime
from .db import orm
from .db import db

class Outage(db.Entity):
    event_id = orm.Required(str, index=True)
    event_status = orm.Required(str)
    event_type = orm.Required(str)
    event_start = orm.Required(datetime, index=True)
    event_stop = orm.Required(datetime, index=True)
    type = orm.Required(str)
    publication_dt = orm.Required(datetime, index=True)
    cap_uom = orm.Required(str)
    unavail_cap = orm.Required(float)
    avail_cap = orm.Required(float)
    instal_cap = orm.Required(float)
    reason = orm.Optional(str)
    fuel = orm.Required(str)
    bid_zone = orm.Required(str)
    asset_name = orm.Required(str)
    mkt_part = orm.Required(str)
    mkt_part_cd = orm.Required(str)
    orm.PrimaryKey(event_id, publication_dt, event_status)

    @classmethod
    def loads(cls, j):
        isofmt = "%Y-%m-%dT%H:%M:%SZ"
        return dict(event_id=j['ns1:messageId'],
                    event_status=j['ns1:event']['ns1:eventStatus'],
                    event_type=j['ns1:event']['ns1:eventType'],
                    event_start=datetime.strptime(
                        j['ns1:event']['ns1:eventStart'], isofmt),
                    event_stop=datetime.strptime(
                        j['ns1:event']['ns1:eventStop'], isofmt),
                    type=j['ns1:unavailabilityType'],
                    publication_dt=datetime.strptime(
                        j['ns1:publicationDateTime'], isofmt),
                    cap_uom=j['ns1:capacity']['ns1:unitMeasure'],
                    unavail_cap=float(
                        j['ns1:capacity']['ns1:unavailableCapacity']),
                    avail_cap=float(j['ns1:capacity']
                                    ['ns1:availableCapacity']),
                    instal_cap=float(j['ns1:capacity']
                                     ['ns1:installedCapacity']),
                    reason=(j['ns1:unavailabilityReason'] or ''),
                    fuel=j['ns1:fuelType'],
                    bid_zone=j['ns1:biddingZone'],
                    asset_name=j['ns1:affectedAsset']['ns2:name'],
                    mkt_part=j['ns1:marketParticipant']['ns2:name'],
                    mkt_part_cd=j['ns1:marketParticipant']['ns2:ace'])

    @classmethod
    def get_or_create(cls, params):
        o = cls.get(**params)
        if o:
            return o
        return cls(**params)

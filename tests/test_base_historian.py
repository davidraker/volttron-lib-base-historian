from datetime import datetime
from time import sleep

from volttron.utils import format_timestamp

from volttron.historian.base import BaseHistorianAgent


class ConcreteHistorianAgent(BaseHistorianAgent):
    def __init__(self, **kwargs):
        super(ConcreteHistorianAgent, self).__init__(**kwargs)
        self._published_list_items = []
        self.start_process_thread()
        sleep(0.5)

    def publish_to_historian(self, to_publish_list):
        self._published_list_items.append(to_publish_list)

    def get_publish_list(self):
        return self._published_list_items

    def reset_publish_list_items(self):
        self._published_list_items.clear()

    def has_published_items(self):
        return len(self._published_list_items) > 0


def test_cache_enable():
    # now = format_timestamp(datetime.utcnow())
    # headers = {
    #     header_mod.DATE: now,
    #     header_mod.TIMESTAMP: now
    # }
    agent = ConcreteHistorianAgent(cache_only_enabled=True)
    assert agent is not None
    device = "devices/testcampus/testbuilding/testdevice"
    agent._capture_data(peer="foo",
                        sender="test",
                        bus="",
                        topic=device,
                        headers={},
                        message={"OutsideAirTemperature": 52.5, "MixedAirTemperature": 58.5},
                        device=device
                        )
    sleep(0.1)
    # Should not have published to the concrete historian because we are in cache_only
    assert not agent.has_published_items()

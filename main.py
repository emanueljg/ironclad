from time import sleep, time

from config import load_config
from calendar import get_events, get_service, search_for_rules


cfg = load_config()


def main():
    service = get_service()
    events = get_events(service)
    refreshed_events_at = 0
    while True:
        now = time()
        if now - refreshed_events_at > cfg['refresh_events']:
            events = get_events(service)
            refreshed_events_at = now

        rules = search_for_rules(events)
        if rules is not None:
            # TODO insert pywin logic
            pass

        sleep(cfg['search_for_rules'])


if __name__ == '__main__':
    main()
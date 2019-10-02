from argh import ArghParser

from .api import VastAPI


def vast():
    vast = VastAPI()

    functionality = [
        vast.change_bid,
        vast.create_instance,
        vast.destroy_instance,
        vast.label_instance,
        vast.list_machine,
        vast.remove_defjob,
        vast.set_defjob,
        vast.set_min_bid,
        vast.show_instances,
        vast.show_machines,
        vast.start_instance,
        vast.stop_instance,
        vast.unlist_machine,
        vast.search_offers
    ]
    p = ArghParser()
    p.add_commands(functionality)
    p.dispatch()


def vast_ai():
    functionality = [
        VastAPI.create_account,
        VastAPI.set_api_key,
        VastAPI.login
    ]
    p = ArghParser()
    p.add_commands(functionality)
    p.dispatch()


if __name__ == '__main__':
    api()

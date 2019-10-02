#!/usr/bin/env python3

from __future__ import unicode_literals, print_function

import json
import os
import requests
import getpass
from requests.utils import requote_uri

from argh import *

from .utils import Query
from .display import Display


try:
    input = raw_input
except NameError:
    pass


class VastAPI(object):
    api_key_location = os.path.expanduser("~/.vast_api_key")
    base_url = "https://vast.ai/api/v0"

    def __init__(self):
        if not os.path.exists(VastAPI.api_key_location):
            print("It appears your API key is not in {loc}, enter your username and password to login".format(loc=VastAPI.api_key_location))
            VastAPI.login()

        with open(VastAPI.api_key_location, 'r') as f:
            self.api_key = f.read().strip()

    def get_url(self, subpath, query_args=None):

        args = {}

        if hasattr(self, 'api_key'):
            args.update({"api_key": self.api_key})
        if query_args is not None:
            args.update(query_args)

        return VastAPI.base_url + subpath + "?" + "&".join(
            "{x}={y}".format(x=x, y=requote_uri(y if isinstance(y, str) else json.dumps(y))) for x, y in args.items())

    @staticmethod
    def login(user=None, password=None):
        if user is None:
            user = input("Username or Email: ")
        if password is None:
            password = getpass.getpass("Password: ")

        url = VastAPI.base_url + "/users/current/"

        r = requests.put(url, json={'username': user, 'password': password})
        r.raise_for_status()
        resp = r.json()
        print("You are user {}! Your existing api key: {}".format(resp["id"], resp["api_key"]))
        VastAPI.set_api_key(resp["api_key"])

    @staticmethod
    def set_api_key(key):
        with open(VastAPI.api_key_location, "w") as f:
            f.write(key)
        print("Your api key has been saved in {}".format(VastAPI.api_key_location))

    def search_offers(self, query="", query_type="on-demand", order='score-', disable_bundling=False, max_rows=100, raw=False):
        query = Query.parse(query, default=True)

        query_order = []
        for name in order.split(","):
            name = name.strip()
            if not name:
                continue
            direction = "asc"
            if name.endswith('-'):
                direction = "desc"
            field = name.strip("-");
            if field in Query.field_alias:
                field = Query.field_alias[field];
            query_order.append([field, direction])

            query["order"] = query_order
            query["type"] = query_type
            query["disable_bundling"] = disable_bundling

        url = self.get_url("/bundles", {"q": query})
        r = requests.get(url)
        r.raise_for_status()
        offers = r.json()["offers"]

        if raw:
            Display.raw(offers)
        else:
            Display.table(offers, max_rows, Display.search_settings)

    def show_instances(self, raw=False, max_rows=100):
        req_url = self.get_url("/instances", {"owner": "me"})
        r = requests.get(req_url)
        r.raise_for_status()
        instances = r.json()["instances"]

        if raw:
            Display.raw(instances)
        else:
            Display.table(instances, max_rows, Display.fields)

    def show_machines(self, raw=False, quiet=False):
        req_url = self.apiurl("/machines", {"owner": "me"})
        r = requests.get(req_url)
        r.raise_for_status()
        rows = r.json()["machines"]

        if raw:
            print(json.dumps(rows, indent=1, sort_keys=True))
        else:
            for machine in rows:
                if quiet:
                    print("{id}".format(id=machine["id"]))
                else:
                    print("{N} machines: ".format(N=len(rows)))
                    print("{id}: {json}".format(id=machine["id"], json=json.dumps(machine, indent=4, sort_keys=True)))

    def list_machine(self, id, price_gpu, price_disk, price_inetu, price_inetd):
        req_url = self.get_url("/machines/create_asks/")

        pricing = {'machine': id, 'price_gpu': price_gpu,
                   'price_disk': price_disk, 'price_inetu': price_inetu,
                   'price_inetd': price_inetd}

        r = requests.put(req_url, json=pricing)

        if r.status_code == 200:
            rj = r.json()
            if rj["success"]:
                print("Offers created for machine id: {id}, @ ${price_gpu}/gpu/day, ${price_inetu}/GB up, ${price_inetd}/GB down".format(**pricing))
            else:
                print(rj["msg"])
        else:
            print("Failed to list machine id: {id} with response code: {r.status_code}, response text: {r.text}".format(**locals()))

    def unlist_machine(self, id):
        req_url = self.get_url("/machines/{machine_id}/asks/".format(machine_id=id))
        r = requests.delete(req_url)

        if r.status_code == 200:
            rj = r.json()
            if rj["success"]:
                print("All offers for machine id: {machine_id} removed, machine delisted.".format(machine_id=id));
            else:
                print(rj["msg"])
        else:
            print("Failed to list machine id: {id} with response code: {r.status_code}, response text: {r.text}".format(**locals()));

    def remove_defjob(self, id):
        req_url = self.get_url("/machines/{machine_id}/defjob/".format(machine_id=id))
        r = requests.delete(req_url);

        if r.status_code == 200:
            rj = r.json();
            if rj["success"]:
                print("Default instance for machine id: {machine_id} removed.".format(machine_id=id))
            else:
                print(rj["msg"])
        else:
            print("Failed to removed default instance for machine id: {id} with response code: {r.status_code}, response text: {r.text}".format(**locals()))

    def start_instance(self, id):
        url = self.get_url(("/instances/{id}/".format(id=id)))
        r = requests.put(url, json={"state": "running"})
        r.raise_for_status()

        if r.status_code == 200:
            rj = r.json()
            if rj["success"]:
                print("Starting instance with machine id: {id}.".format(**(locals())))
            else:
                print(rj["msg"])
        else:
            print("Failed to start instance for machine id: {id} with error {r.status_code}, response text: {r.text}".format(**locals()))

    def stop_instance(self, id):
        url = self.get_url("/instances/{id}/".format(id=id))
        r = requests.put(url, json={"state": "stopped"})
        r.raise_for_status()

        if r.status_code == 200:
            rj = r.json()
            if rj["success"]:
                print("Stopping instance with machine id: {id}.".format(**(locals())))
            else:
                print(rj["msg"])
        else:
            print("Failed to stop instance for machine id: {id} with error {r.status_code}, response text: {r.text}".format(**locals()))

    def label_instance(self, id, label):
        url = self.get_url("/instances/{id}/".format(id=id))
        r = requests.put(url, json={"label": label})
        r.raise_for_status()

        if r.status_code == 200:
            rj = r.json()
            if rj["success"]:
                print("Label for instance with machine id: {id} set to: {label}.".format(**(locals())))
            else:
                print(rj["msg"])
        else:
            print("Failed to label instance for machine id: {id} with error {r.status_code}, response text: {r.text}".format(**locals()))

    def destroy_instance(self, id):
        url = self.get_url("/instances/{id}/".format(id=id))
        r = requests.delete(url, json={})
        r.raise_for_status()

        if r.status_code == 200:
            rj = r.json()
            if rj["success"]:
                print("Destroying instance with machine id: {id}.".format(**(locals())))
            else:
                print(rj["msg"])
        else:
            print("Failed to destroy instance for machine id: {id} with error {r.status_code}, response text: {r.text}".format(**locals()))

    def set_defjob(self, id, price_gpu, price_inetu, price_inetd, image, args):
        req_url = self.get_url("/machines/create_bids/")

        r = requests.put(req_url, json={
            'machine': id, 'price_gpu': price_gpu,
            'price_inetu': price_inetu, 'price_inetd': price_inetd,
            'image': image, 'args': args
        })

        if r.status_code == 200:
            rj = r.json()
            if rj["success"]:
                print("Created bids for instance with machine id: {id}, @ ${price_gpu}/gpu/day, ${price_inetu}/GB up, ${price_inetd}/GB down".format(**locals()))
            else:
                print(rj["msg"])
        else:
            print("Failed to create bids on instance with machine id: {id} with error {r.status_code}, response text: {r.text}".format(**locals()));

    def create_instance(self, id, image, price, label, disk=10, create_from_id=None,
                        runtype='ssh', onstart=None, onstart_cmd=None,
                        use_jupyer_lab=False, jupyter_dir=None,
                        python_utf8=False, force=False,  extra=None,):
        if onstart:
            with open(onstart, "r") as f:
                onstart_cmd = f.read()

        if jupyter_dir or use_jupyer_lab:
            runtype = 'jupyter'

        url = self.get_url("/asks/{id}/".format(id=id))
        r = requests.put(url, json={
            "client_id": "me",
            "image": image,
            "args": None,
            "price": price,
            "disk": disk,
            "label": label,
            "extra": extra,
            "onstart": onstart_cmd,
            "runtype": runtype,
            "python_utf8": python_utf8,
            "lang_utf8": None,
            "use_jupyter_lab": use_jupyer_lab,
            "jupyter_dir": jupyter_dir,
            "create_from": create_from_id,
            "force": force
        })
        r.raise_for_status()
        print(Display.raw(r.json()))

    def change_bid(self, id, price):
        url = self.get_url("/instances/bid_price/{id}/".format(id=id))
        r = requests.put(url, json={"client_id": "me", "price": price})
        r.raise_for_status()
        print("Per gpu bid price changed to {price}".format(**locals()))

    def set_min_bid(self, id, price):
        url = self.get_url("/machines/{id}/minbid/".format(id=id))
        r = requests.put(url, json={"client_id": "me", "price": price})
        r.raise_for_status()
        print("Per gpu min bid price changed to {price}".format(**locals()))

    @staticmethod
    def create_account(email=None, user=None, password=None, ssh_key_path=None):
        if email is None:
            email = input("Email: ")
        if user is None:
            user = input("Username: ")
        if password is None:
            password = getpass.getpass("Password: ")
        if ssh_key_path is None:
            ssh_key = None
            ssh_key_path = input("Optional ssh key path: ")
            if ssh_key_path:
                if not os.path.exists(ssh_key_path):
                    print("Couldn't find SSH key in location {ssh_key_path}".format(ssh_key_path=ssh_key_path))
                else:
                    with open(ssh_key_path, 'r') as f:
                        ssh_key = f.read()

        url = VastAPI.base_url + "/users/"
        r = requests.post(url, json={"email": email, "username": user, "password":  password, "ssh_key": ssh_key})
        r.raise_for_status()
        resp = r.json()

        print("You are user {id}! Your new api key: {api_key}".format(**resp))
        VastAPI.set_api_key(resp["api_key"])


if __name__ == "__main__":
    api = VastAPI()
    # print(Query.parse("compute_cap > 610 total_flops < 5 verified = False"))
    api.search_offers()

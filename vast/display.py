import json

#import pandas as pd

identity = lambda x: x

class Display:

    search_settings = (
        ("id", "ID", "{}", identity, True),
        ("cuda_max_good", "CUDA", "{:0.1f}", identity, True),
        ("num_gpus", "Num", "{} x", identity, False),
        ("gpu_name", "Model", "{}", identity, True),
        ("pcie_bw", "PCIE BW", "{:0.1f}", identity, True),
        ("cpu_cores_effective", "vCPUs", "{:0.1f}", identity, True),
        ("cpu_ram", "RAM", "{:0.1f}", lambda x: x / 1000, False),
        ("disk_space", "Storage", "{:.0f}", identity, True),
        ("dph_total", "$/hr", "{:0.4f}", identity, True),
        ("dlperf", "DLPerf", "{:0.1f}", identity, True),
        ("dlperf_per_dphtotal", "DLP/$", "{:0.1f}", identity, True),
        ("inet_up", "Net up", "{:0.1f}", identity, True),
        ("inet_down", "Net down", "{:0.1f}", identity, True),
        ("reliability2", "R", "{:0.1f}", lambda x: x * 100, True),
        ("duration", "Max Days", "{:0.1f}", lambda x: x / (24.0 * 60.0 * 60.0), True),
        ("min_bid", "Min Bid", "{:0.3f}", identity, False),
    )

    fields = (
        ("id", "ID", "{}", None, True),
        ("machine_id", "Machine", "{}", None, True),
        ("actual_status", "Status", "{}", None, True),
        ("num_gpus", "Num", "{} x", None, False),
        ("gpu_name", "Model", "{}", None, True),
        ("gpu_util", "Util. %", "{:0.1f}", None, True),
        ("cpu_cores_effective", "vCPUs", "{:0.1f}", None, True),
        ("cpu_ram", "RAM", "{:0.1f}", lambda x: x / 1000, False),
        ("disk_space", "Storage", "{:.0f}", None, True),
        ("ssh_host", "SSH Addr", "{}", None, True),
        ("ssh_port", "SSH Port", "{}", None, True),
        ("dph_total", "$/hr", "{:0.4f}", None, True),
        ("image_uuid", "Image", "{}", None, True),

        # ("dlperf",              "DLPerf",   "{:0.1f}",  None, True),
        # ("dlperf_per_dphtotal", "DLP/$",    "{:0.1f}",  None, True),
        ("inet_up", "Net up", "{:0.1f}", None, True),
        ("inet_down", "Net down", "{:0.1f}", None, True),
        ("reliability2", "R", "{:0.1f}", lambda x: x * 100, True),
        # ("duration",            "Max Days", "{:0.1f}",  lambda x: x/(24.0*60.0*60.0), True),
    )

    @staticmethod
    def raw(data):
        print(json.dumps(data, indent=2, sort_keys=True))

    # @staticmethod
    # def table(data, max_rows, settings=None):
    #     df = pd.DataFrame(data)
    #     if settings:
    #         # Subset
    #         df = df[[col[0] for col in settings]]
    #         # Rename
    #         df = df.rename(columns={col[0]: col[1] for col in settings})
    #         # Transform
    #         for col in settings:
    #             df.loc[:, col[1]] = df[col[1]].map(col[3]).map(col[2].format, na_action='ignore')
    #
    #     df = df.fillna('-')
    #
    #     if max_rows:
    #         df = df.head(max_rows)
    #
    #     print(df.to_string(index=False))

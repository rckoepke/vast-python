import re


class Query:

    op_names = [
        ([">=", "gte"], "gte"),
        ([">", "gt"], "gt"),
        (["<=", "lte"], "lte"),
        (["<", "lt"], "lt"),
        (["!=", "neq", "noteq", "not eq"], "neq"),
        (["==", "=", "eq"], "eq"),
        (["notin", "not in", "nin"], "notin"),
        (["in"], "notin"),
    ]
    op_names = {key: opt[1] for opt in op_names for key in opt[0]}

    field_alias = {
        "cuda_vers": "cuda_max_good",
        "display_active": "gpu_display_active",
        "reliability": "reliability2",
        "dlperf_usd": "dlperf_per_dphtotal",
        "dph": "dph_total",
        "flops_usd": "flops_per_dphtotal",
    }

    field_multiplier = {
        "cpu_ram": 1000,
        "duration": 1.0 / (24.0 * 60.0 * 60.0),
    }

    fields = {
        "compute_cap",
        "cpu_cores",
        "cpu_cores_effective",
        "cpu_ram",
        "cuda_max_good",
        "disk_bw",
        "disk_space",
        "dlperf",
        "dlperf_per_dphtotal"
        "dph_total",
        "duration",
        "external",
        "flops_per_dphtotal",
        "gpu_display_active",
        # "gpu_ram_free_min",
        "gpu_mem_bw",
        "gpu_name",
        "gpu_ram",
        "has_avx",
        "host_id",
        "id",
        "inet_down",
        "inet_down_cost",
        "inet_up",
        "inet_up_cost",
        "min_bid",
        "mobo_name",
        "num_gpus",
        "pci_gen",
        "pcie_bw",
        "reliability2",
        "rentable",
        "rented",
        "storage_cost",
        "total_flops",
        "verified"
    }

    @staticmethod
    def parse(query, default=True):

        res = {}
        if default:
            res = {"verified": {"eq":  True}, "external": {"eq": False}, "rentable": {"eq": True}}

        if type(query) == list:
            query = " ".join(query)
            query = query.strip()
        opts = re.findall("([a-zA-Z0-9_]+)( *[=><!]+| +(?:[lg]te?|nin|neq|eq|not ?eq|not ?in|in) )?( *)(\[[^\]]+\]|[^ ]+)?( *)", query)

        # Check that all the options are parsed correctly
        joined = "".join("".join(x) for x in opts)
        if joined != query:
            raise ValueError(
                "Unconsumed text. Did you forget to quote your query? " + repr(joined) + " != " + repr(query))

        for field, op, _, value, _ in opts:
            value = value.strip(",[]")
            v = res.setdefault(field, {})
            op = op.strip()

            if not value:
                raise ValueError("Value cannot be blank. Did you forget to quote your query? " + repr((field, op, value)))
            if not field:
                raise ValueError("Field cannot be blank. Did you forget to quote your query? " + repr((field, op, value)))

            op_name = Query.op_names.get(op)

            field_name = Query.field_alias.get(field)

            if (field not in Query.fields) and (field_name not in Query.fields):
                print("Warning: Unrecognized field: {}, see list of recognized fields.".format(field))
            if not op_name:
                raise ValueError("Unknown operator. Did you forget to quote your query? " + repr(op).strip("u"))

            if op_name in ["in", "notin"]:
                value = [x.strip() for x in value.split(",") if x.strip()]

            if value in ["?", "*", "any"]:
                if op_name != "eq":
                    raise ValueError("Wildcard only makes sense with equals.")
                if field in v:
                    del v[field]
                if field in res:
                    del res[field]
                continue

            if field in Query.field_multiplier:
                value = str(float(value) * Query.field_multiplier[field])

            v[op_name] = value
            res[field] = v

        return res

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long, too-many-statements


def load_arguments(self, _):

    from knack.arguments import CLIArgumentType
    from azure.cli.core.commands.parameters import tags_type, get_three_state_flag, get_enum_type
    from azure.cli.core.commands.validators import get_default_location_from_resource_group, validate_file_or_dict
    from ._validators import process_missing_resource_group_parameter
    from azext_amg.vendored_sdks.models import ZoneRedundancy
    grafana_name_type = CLIArgumentType(options_list="--grafana-name",
                                        help="Name of the Azure Managed Grafana.",
                                        id_part="name")
    grafana_role_type = CLIArgumentType(arg_type=get_enum_type(["Admin", "Editor", "Viewer"]), options_list=["--role", "-r"],
                                        help="Grafana role name")

    with self.argument_context("grafana") as c:
        c.argument("tags", tags_type)
        c.argument("location", validator=get_default_location_from_resource_group)
        c.argument("grafana_name", grafana_name_type, options_list=["--name", "-n"], id_part=None, validator=process_missing_resource_group_parameter)
        c.argument("id", help=("The identifier (id) of a dashboard/data source is an auto-incrementing "
                               "numeric value and is only unique per Grafana install."))
        c.argument("folder", help="id, uid, title which can identify a folder. CLI will search in the order of id, uid, and title, till finds a match")
        c.argument("api_key_or_token", options_list=["--api-key", "--token", '-t'],
                   help="api key or service account token, a randomly generated string used to interact with Grafana endpoint; if missing, CLI will use logon user's credentials")

    with self.argument_context("grafana create") as c:
        c.argument("grafana_name", grafana_name_type, options_list=["--name", "-n"], validator=None)
        c.argument("zone_redundancy", arg_type=get_enum_type(ZoneRedundancy), help="Indicates whether or not zone redundancy should be enabled. Default: Disabled")
        c.argument("skip_system_assigned_identity", options_list=["-s", "--skip-system-assigned-identity"], arg_type=get_three_state_flag(), help="Do not enable system assigned identity")
        c.argument("skip_role_assignments", arg_type=get_three_state_flag(), help="Do not create role assignments for managed identity and the current login user")
        c.argument("principal_ids", nargs="+", help="space-separated Azure AD object ids for users, groups, etc to be made as Grafana Admins. Once provided, CLI won't make the current logon user as Grafana Admin")

    # api_key=None, deterministic_outbound_ip=None, public_network_access=None
    with self.argument_context("grafana update") as c:
        c.argument("api_key_and_service_account", get_enum_type(["Enabled", "Disabled"]), options_list=['--api-key', '--service-account'],
                   help="If enabled, you will be able to configur Grafana api keys and service accounts")
        c.argument("deterministic_outbound_ip", get_enum_type(["Enabled", "Disabled"]), options_list=["-i", "--deterministic-outbound-ip"],
                   help="if enabled, the Grafana workspace will have fixed egress IPs you can use them in the firewall of datasources")

    with self.argument_context("grafana dashboard") as c:
        c.argument("uid", options_list=["--dashboard"], help="dashboard uid")
        c.argument("title", help="title of a dashboard")
        c.argument('overwrite', arg_type=get_three_state_flag(), help='Overwrite a dashboard with same uid')

    with self.argument_context("grafana dashboard create") as c:
        c.argument("definition", type=validate_file_or_dict, help="The complete dashboard model in json string, a path or url to a file with such content")

    with self.argument_context("grafana dashboard update") as c:
        c.argument("definition", type=validate_file_or_dict, help="The complete dashboard model in json string, a path or url to a file with such content")

    with self.argument_context("grafana dashboard import") as c:
        c.argument("definition", help="The complete dashboard model in json string, Grafana gallery id, a path or url to a file with such content")

    with self.argument_context("grafana") as c:
        c.argument("time_to_live", default="1d", help="The life duration. For example, 1d if your key is going to last fr one day. Supported units are: s,m,h,d,w,M,y")

    with self.argument_context("grafana api-key") as c:
        c.argument("key_name", help="api key name")
        c.argument("role", grafana_role_type, default="Viewer")
        c.argument("time_to_live", default="1d", help="The API key life duration. For example, 1d if your key is going to last fr one day. Supported units are: s,m,h,d,w,M,y")

    with self.argument_context("grafana api-key create") as c:
        c.argument("key", help="api key name")

    with self.argument_context("grafana api-key delete") as c:
        c.argument("key", help="id or name that identify an api-key to delete")

    with self.argument_context("grafana data-source") as c:
        c.argument("data_source", help="name, id, uid which can identify a data source. CLI will search in the order of name, id, and uid, till finds a match")
        c.argument("definition", type=validate_file_or_dict, help="json string with data source definition, or a path to a file with such content")

    with self.argument_context("grafana notification-channel") as c:
        c.argument("notification_channel", help="id, uid which can identify a data source. CLI will search in the order of id, and uid, till finds a match")
        c.argument("definition", type=validate_file_or_dict, help="json string with notification channel definition, or a path to a file with such content")
        c.argument("short", action='store_true', help="list notification channels in short format.")

    with self.argument_context("grafana data-source query") as c:
        c.argument("conditions", nargs="+", help="space-separated condition in a format of `<name>=<value>`")
        c.argument("time_from", options_list=["--from"], help="start time in iso 8601, e.g. '2022-01-02T16:15:00'. Default: 1 hour early")
        c.argument("time_to", options_list=["--to"], help="end time in iso 8601, e.g. '2022-01-02T17:15:00'. Default: current time ")
        c.argument("max_data_points", type=int, help="Maximum amount of data points that dashboard panel can render. Default: 1000")
        c.argument("query_format", help="format of the resule, e.g. table, time_series")
        c.argument("internal_ms", type=int, help="The time interval in milliseconds of time series. Default: 1000")

    with self.argument_context("grafana folder") as c:
        c.argument("title", help="title of the folder")

    with self.argument_context("grafana user") as c:
        c.argument("user", help="user login name or email")

    with self.argument_context("grafana service-account") as c:
        c.argument("service_account", help="id or name which can identify a service account")
        c.argument("is_disabled", arg_type=get_three_state_flag(), help="disable the service account. default: false")

    with self.argument_context("grafana service-account create") as c:
        c.argument("role", grafana_role_type, default="Viewer")
        c.argument("service_account", help="service account name")

    with self.argument_context("grafana service-account update") as c:
        c.argument("role", grafana_role_type)
        c.argument("new_name", help="new name of the service account")

    with self.argument_context("grafana service-account token") as c:
        c.argument("token", help="id or name which can identify a service account token")

    with self.argument_context("grafana service-account token create") as c:
        c.argument("token", help="name of the new service account token")

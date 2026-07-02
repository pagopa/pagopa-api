data "github_organization_teams" "all" {
  root_teams_only = true
  summary_only    = true
}


data "azurerm_resource_group" "apim_resource_group" {
  name = "${local.product}-api-rg"
}

data "azurerm_user_assigned_identity" "identity_ci_01"{
  name = "${local.prefix}-${var.env_short}-${local.domain}-01-github-ci-identity"
  resource_group_name = "${local.prefix}-${var.env_short}-identity-rg"
}


---
description: "Source references and maintenance manifest for the group guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Web Sources

| Source | URL | Date accessed |
|---|---|---|
| Group module project page | https://www.drupal.org/project/group | 2026-03-10 |
| Group Action module project page | https://www.drupal.org/project/group_action | 2026-03-10 |
| Upgrading from v1 to v2 guide | https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/group/group-v2v3-guides/upgrading-from-v1-to-v2 | 2026-03-10 |
| Group 2.x to 3.x migration issue | https://www.drupal.org/project/group/issues/3362037 | 2026-03-10 |
| Group::addContent() rename change record | https://www.drupal.org/node/3292844 | 2026-03-10 |
| Group 2.0.0 release notes | https://www.drupal.org/project/group/releases/2.0.0 | 2026-03-10 |
| Group 4.0.0-alpha1 release | https://www.drupal.org/project/group/releases/4.0.0-alpha1 | 2026-05-20 |
| Group 4.0.0-alpha2 release | https://www.drupal.org/project/group/releases/4.0.0-alpha2 | 2026-09-01 |
| GroupRelationshipType at 4.0.0-alpha2 (relation_type rename) | https://git.drupalcode.org/project/group/-/raw/4.0.0-alpha2/src/Entity/GroupRelationshipType.php | 2026-09-01 |
| Group 4.0.x change records | https://www.drupal.org/list-changes/group/published?to_branch=4.0.x | 2026-05-20 |
| Group 3.3.5 release | https://www.drupal.org/project/group/releases/3.3.5 | 2026-05-20 |
| Group release history feed (branches, tags, core compatibility) | https://updates.drupal.org/release-history/group/current | 2026-08-16 |
| `group_action` release history | https://updates.drupal.org/release-history/group_action/current | 2026-08-16 |
| `group_content_menu` release history | https://updates.drupal.org/release-history/group_content_menu/current | 2026-08-16 |
| `group_permissions` release history | https://updates.drupal.org/release-history/group_permissions/current | 2026-08-16 |
| `subgroup` release history | https://updates.drupal.org/release-history/subgroup/current | 2026-08-16 |
| `group_flex` release history | https://updates.drupal.org/release-history/group_flex/current | 2026-08-16 |
| `group2to3` project page | https://www.drupal.org/project/group2to3 | 2026-08-16 |

## Code Sources

Primary source analysis for the 4.x update conducted against **Group tag `4.0.0-alpha2`** (git `git.drupalcode.org/project/group`), cross-referenced with `4.0.0-alpha1` for what the rename changed and with Group 3.3.5 for the `3.x:` callouts. The tag is pinned deliberately rather than a 4.0.x branch commit: this guide documents tagged releases only. Refreshed 2026-09-01 — the `content_plugin` → `relation_type` rename that the previous revision recorded as unreleased shipped in `alpha2`, verified by reading the entity class at both tags.

| Path | Covers |
|---|---|
| `src/Hook/*.php` | OOP hook classes — hooks, query alters, form alters, user cancel/delete (replaces the deleted `group.module`) |
| `group.services.yml` | All service definitions, handlers, and `access_policy`-tagged services |
| `group.group.permissions.yml` | Core group permissions |
| `group.api.php` | Documented hook API |
| `src/Entity/Group.php` | Group entity, baseFieldDefinitions, member/relationship API |
| `src/Entity/GroupInterface.php` | Group entity interface contract |
| `src/Entity/GroupRelationship.php` | GroupRelationship entity |
| `src/Entity/GroupRelationshipInterface.php` | GroupRelationship interface contract |
| `src/Entity/GroupRelationshipType.php` | Internal bundle entity for relationships |
| `src/Entity/GroupRole.php` | Role config entity, scope system |
| `src/Entity/GroupRoleInterface.php` | Role interface |
| `src/Entity/GroupType.php` | Group type config entity |
| `src/Entity/GroupTypeInterface.php` | Group type interface |
| `src/Entity/GroupMembership.php` | Shared bundle class for memberships |
| `src/Entity/Storage/GroupRelationshipStorage.php` | Storage with loadByGroup/Entity/Plugin methods |
| `src/Entity/Access/GroupAccessControlHandler.php` | Group entity access handler |
| `src/Entity/Views/GroupViewsData.php` | Group Views data |
| `src/Entity/Views/GroupRelationshipViewsData.php` | GroupRelationship Views data |
| `src/Plugin/Attribute/GroupRelationType.php` | PHP 8 attribute for plugin discovery |
| `src/Plugin/Group/Relation/GroupRelationBase.php` | Base plugin class, configuration form |
| `src/Plugin/Group/Relation/GroupRelationType.php` | Plugin definition/metadata class |
| `src/Plugin/Group/Relation/GroupRelationTypeManagerInterface.php` | Plugin manager interface |
| `src/Plugin/Group/Relation/GroupMembership.php` | group_membership plugin |
| `src/Plugin/Group/RelationHandlerDefault/AccessControl.php` | Default access control handler |
| `src/Plugin/Group/RelationHandlerDefault/PermissionProvider.php` | Default permission provider |
| `src/PermissionScopeInterface.php` | Scope constants |
| `src/Entity/GroupMembershipTrait.php` | Static membership load methods, array `$roles` filter, caching |
| `src/Access/GroupPermissionHandler.php` | Permission YAML discovery |
| `src/Access/GroupPermissionCalculator.php` | Aggregates all scopes via core's `access_policy_processor` |
| `src/Access/GroupPermissionsHashGenerator.php` | Permission hash for cache vary |
| `src/Access/GroupAccessResult.php` | Cache-aware access result |
| `src/Access/IndividualGroupRoleAccessPolicy.php` | Individual-scope access policy (Access Policy API) |
| `src/Access/SynchronizedGroupRoleAccessPolicy.php` | Outsider/insider-scope access policy (Access Policy API) |
| `src/QueryAccess/EntityQueryAlter.php` | Entity query access filtering |
| `src/EventSubscriber/AnonymousUserResponseSubscriber.php` | Anonymous cache tag injection |
| `src/Plugin/Block/GroupOperationsBlock.php` | Group operations block |
| `modules/gnode/` | Group Node sub-module |
| `modules/group_support_revisions/` | Revision access sub-module |
| `config/schema/group.schema.yml` | Full config schema |
| `group.views.inc` | Views data alter hooks |
| `group_action/src/Plugin/Action/GroupActionBase.php` | Base action class, execute/access/config logic |
| `group_action/src/Plugin/Action/GroupActionDeriver.php` | Per-entity-type derivative discovery |
| `group_action/src/Plugin/Action/GroupAdd*.php` | Add content/member action plugins |
| `group_action/src/Plugin/Action/GroupRemove*.php` | Remove content/member action plugins |
| `group_action/src/Plugin/Action/GroupUpdate*.php` | Update content/member action plugins |
| `group_action/src/Compatibility.php` | ECA recursion threshold workaround |

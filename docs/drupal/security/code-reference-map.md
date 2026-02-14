---
description: Quick lookup table for security-related classes, interfaces, and file paths in Drupal core organized by subsystem.
---

# Code Reference Map

## When to Use
Quick lookup for where to find security-related code in Drupal core.

## Items

### Access System
| Component | Path |
|---|---|
| AccessResult | `/core/lib/Drupal/Core/Access/AccessResult.php` |
| AccessResultInterface | `/core/lib/Drupal/Core/Access/AccessResultInterface.php` |
| AccessManagerInterface | `/core/lib/Drupal/Core/Access/AccessManagerInterface.php` |
| AccessCheckInterface | `/core/lib/Drupal/Core/Access/AccessCheckInterface.php` |
| CsrfTokenGenerator | `/core/lib/Drupal/Core/Access/CsrfTokenGenerator.php` |
| CsrfAccessCheck | `/core/lib/Drupal/Core/Access/CsrfAccessCheck.php` |
| EntityAccessControlHandler | `/core/lib/Drupal/Core/Entity/EntityAccessControlHandler.php` |

### XSS Prevention
| Component | Path |
|---|---|
| Xss utility | `/core/lib/Drupal/Component/Utility/Xss.php` |
| Html utility | `/core/lib/Drupal/Component/Utility/Html.php` |
| MarkupInterface | `/core/lib/Drupal/Component/Render/MarkupInterface.php` |
| Markup class | `/core/lib/Drupal/Component/Render/Markup.php` |
| UrlHelper | `/core/lib/Drupal/Component/Utility/UrlHelper.php` |

### Database Security
| Component | Path |
|---|---|
| Connection (Database API) | `/core/lib/Drupal/Core/Database/Connection.php` |
| Select query builder | `/core/lib/Drupal/Core/Database/Query/Select.php` |
| SelectInterface | `/core/lib/Drupal/Core/Database/Query/SelectInterface.php` |

### Authentication and Sessions
| Component | Path |
|---|---|
| AuthenticationManager | `/core/lib/Drupal/Core/Authentication/AuthenticationManager.php` |
| AuthenticationProviderInterface | `/core/lib/Drupal/Core/Authentication/AuthenticationProviderInterface.php` |
| SessionManager | `/core/lib/Drupal/Core/Session/SessionManager.php` |
| AccountInterface | `/core/lib/Drupal/Core/Session/AccountInterface.php` |
| User entity | `/core/modules/user/src/Entity/User.php` |
| PasswordInterface | `/core/lib/Drupal/Core/Password/PasswordInterface.php` |

### Permissions and Roles
| Component | Path |
|---|---|
| PermissionHandler | `/core/modules/user/src/PermissionHandler.php` |
| PermissionHandlerInterface | `/core/modules/user/src/PermissionHandlerInterface.php` |
| Role entity | `/core/modules/user/src/Entity/Role.php` |

### Trusted Callbacks
| Component | Path |
|---|---|
| TrustedCallbackInterface | `/core/lib/Drupal/Core/Security/TrustedCallbackInterface.php` |
| DoTrustedCallbackTrait | `/core/lib/Drupal/Core/Security/DoTrustedCallbackTrait.php` |
| TrustedCallback attribute | `/core/lib/Drupal/Core/Security/Attribute/TrustedCallback.php` |

### Request Sanitization
| Component | Path |
|---|---|
| RequestSanitizer | `/core/lib/Drupal/Core/Security/RequestSanitizer.php` |

### File Handling
| Component | Path |
|---|---|
| FileUploadHandler | `/core/modules/file/src/Upload/FileUploadHandler.php` |
| FileExtensionValidator | `/core/modules/file/src/Validation/FileExtensionValidator.php` |
| FileSizeValidator | `/core/modules/file/src/Validation/FileSizeValidator.php` |

### Validation
| Component | Path |
|---|---|
| EmailValidator service | `/core/lib/Drupal/Core/Validation/Plugin/Validation/Constraint/` |
| Form validation | `/core/lib/Drupal/Core/Form/FormValidator.php` |

### Node Access
| Component | Path |
|---|---|
| Node module (grants hooks) | `/core/modules/node/node.module` |
| NodeAccessControlHandler | `/core/modules/node/src/NodeAccessControlHandler.php` |

## Common Mistakes
- Reading code without running it -- Use debugger, add `var_dump()`, trace execution
- Not checking PHPDoc -- Documentation often explains "why" not just "what"
- Assuming code is current -- Verify you're reading the right Drupal version

## See Also
- Reference: https://api.drupal.org/api/drupal (API documentation)

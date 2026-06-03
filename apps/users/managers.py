from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _validate_normal_user(self, branch, role):
        """
        Legacy placeholder - validation is handled in `_create_user`.
        Kept for backward compatibility.
        """
        return

    def _create_user(self, email_id, password=None, **extra_fields):
        """
        Create a user (regular or superuser).
        - Superusers: branch, tenant, and role can be NULL (Platform Admin)
        - Regular users: must have branch and role
        """
        if not email_id:
            raise ValueError('The email_id field is required.')

        email_id = self.normalize_email(email_id)
        
        # Check if this is a superuser (gets value from extra_fields or defaults to False)
        is_superuser = extra_fields.get('is_superuser', False)

        # Validate normal users according to role rules
        if not is_superuser:
            branch = extra_fields.get('branch')
            role = extra_fields.get('role')
            if not role:
                raise ValueError('A role is required for tenant users.')

            # Company admin: tenant required, branch optional
            if role == self.model.Role.COMPANY_ADMIN:
                tenant = extra_fields.get('tenant')
                if tenant is None and branch is None:
                    raise ValueError('A tenant or branch is required for company admin users.')
                # derive tenant from branch if provided and tenant not provided
                if 'tenant' not in extra_fields and branch is not None:
                    extra_fields['tenant'] = branch.tenant
                # if both provided ensure consistency
                if ('tenant' in extra_fields) and branch is not None and branch.tenant_id != extra_fields['tenant'].tenant_id:
                    raise ValueError('Branch must belong to the provided tenant.')

            # Manager, Technician, Receptionist: require branch and tenant
            elif role in (self.model.Role.MANAGER, self.model.Role.TECHNICIAN, self.model.Role.RECEPTIONIST):
                if branch is None:
                    raise ValueError('A branch is required for users with this role.')
                if 'tenant' not in extra_fields or extra_fields.get('tenant') is None:
                    extra_fields['tenant'] = branch.tenant
                # ensure branch belongs to tenant
                if extra_fields.get('tenant') and branch.tenant_id != extra_fields['tenant'].tenant_id:
                    raise ValueError('Branch must belong to the provided tenant.')
            else:
                raise ValueError('Invalid role specified.')
        else:
            # Superusers: ensure tenant and branch are NULL
            extra_fields['tenant'] = None
            extra_fields['branch'] = None

        user = self.model(email_id=email_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email_id, password=None, **extra_fields):
        """
        Create a regular tenant user.
        Requires: branch, role, mobile_num
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email_id, password, **extra_fields)

    def create_superuser(self, email_id, password=None, **extra_fields):
        """
        Create a platform administrator (superuser).
        Superuser has NO branch or tenant.
        Superuser is NOT a tenant user.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        # Explicitly set to None for superuser
        extra_fields['tenant'] = None
        extra_fields['branch'] = None
        extra_fields['role'] = ''

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email_id, password, **extra_fields)

from utils.prepare_vault import prepare_vault


VAULT = 'vault'
TEMP_VAULT = '.vault_prepared'


if __name__ == "__main__":

    prepare_vault(VAULT, TEMP_VAULT)

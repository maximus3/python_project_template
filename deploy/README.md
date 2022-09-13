# How generate files to deploy?

## 1. Generate files

```bash
echo YOUR_HOSTNAME > host.txt
echo YOUR_USERNAME > username.txt
```

## 2. Generate files

```bash
chmod +x generate.sh
./generate.sh
```

## 3. Add Github/Gitlab Secrets

- `.env` to `ENV`
- `known_hosts_to_github.txt` to `SSH_KNOWN_HOSTS`
- `host.txt` to `SSH_ADRESS`
- `username.txt` to `SSH_USERNAME`
- `id_rsa` to `SSH_KEY`

### How to add secrets in GitHub?

- Open `Settings` of your repo
- Open `Secrets` - `Actions`
- Click on `New repository secret`

## 4. Security

**MAKE SURE YOU DON'T COMMIT THE GENERATED FILES TO THE REPOSITORY**

CHECK `.gitignore`

---
name: ssh-key-deploy
description: Set up, verify, and troubleshoot SSH key based login from the local machine to a Linux server. Use when the user asks to connect to a server with SSH, generate a key pair, append a public key to authorized_keys, test passwordless login, prepare deployment access, or fix publickey authentication failures without exposing private keys.
---

# SSH Key Deploy

## Goal

Establish passwordless SSH access from the current local machine to a remote Linux server using a dedicated key pair, then verify the exact user, host, and working directory before performing any deployment work.

Never print or transmit a private key. It is safe to show a public key and a one-line `authorized_keys` append command.

## Workflow

1. Collect the target:
   - `user`: usually `root` or a deployment user.
   - `host`: IP or hostname.
   - `key_name`: use a project-specific name such as `smartbid_deploy_rsa`.

2. Check basic network reachability before changing keys.

   PowerShell:
   ```powershell
   Test-NetConnection <host> -Port 22
   ```

   SSH quick check:
   ```powershell
   ssh -o BatchMode=yes -o ConnectTimeout=8 <user>@<host> "echo ok"
   ```

3. Generate a dedicated local key pair if one does not already exist.

   Prefer RSA 4096 when compatibility is uncertain:
   ```powershell
   $key = "$env:USERPROFILE\.ssh\<key_name>"
   if (-not (Test-Path $key)) {
     ssh-keygen --% -t rsa -b 4096 -f C:\Users\Administrator\.ssh\<key_name> -N "" -C <key_name>
   }
   Get-Content "$key.pub"
   ```

   Use Ed25519 only when the server and local OpenSSH versions are known to support it reliably:
   ```powershell
   ssh-keygen --% -t ed25519 -f C:\Users\Administrator\.ssh\<key_name> -N "" -C <key_name>
   ```

4. Give the user a server-side append command using the public key only.

   Linux server command:
   ```bash
   mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '<PUBLIC_KEY_LINE>' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
   ```

   If connected as a non-target user, append to the target user's home:
   ```bash
   sudo mkdir -p /home/<user>/.ssh
   echo '<PUBLIC_KEY_LINE>' | sudo tee -a /home/<user>/.ssh/authorized_keys >/dev/null
   sudo chown -R <user>:<user> /home/<user>/.ssh
   sudo chmod 700 /home/<user>/.ssh
   sudo chmod 600 /home/<user>/.ssh/authorized_keys
   ```

5. Verify passwordless login from the local machine.

   ```powershell
   ssh -i C:\Users\Administrator\.ssh\<key_name> -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=12 <user>@<host> "hostname && whoami && pwd"
   ```

   Success criteria:
   - exit code is `0`
   - output hostname is the expected server
   - `whoami` matches the target user
   - no password prompt appears

6. For deployment, run a harmless directory check before upload or mutation.

   ```powershell
   ssh -i C:\Users\Administrator\.ssh\<key_name> -o IdentitiesOnly=yes -o StrictHostKeyChecking=no <user>@<host> "pwd && ls -la /opt || true"
   ```

## Troubleshooting

- `Permission denied (publickey,...)`: the key is not accepted or not authorized for that user. Re-check the exact remote user and `authorized_keys` location.
- Server says it "accepts key" in `ssh -vvv` but login still fails: try an RSA 4096 key. Older Windows OpenSSH and some server policies can behave poorly with Ed25519.
- Password login works but key login fails: that only proves network and credentials are fine; it does not prove the public key was installed for the same user.
- `Get-Content: command not found` on the server: `Get-Content` is a local PowerShell command. Read the public key locally, then paste only the public key into a Linux `echo ... >> ~/.ssh/authorized_keys` command.
- When sending Linux commands through PowerShell SSH, protect remote shell variables from local expansion. Prefer single quotes around the remote command, or escape `$`. For example, `$(date ...)` inside double quotes is expanded by PowerShell locally.
- If `Test-NetConnection` times out but the user can connect elsewhere, verify firewall/security-group rules and whether the local network allows outbound port 22.

## Safety Rules

- Do not output private key files such as `<key_name>`; only output `<key_name>.pub`.
- Do not overwrite `authorized_keys`; append to it.
- Do not loosen remote permissions beyond `700` for `.ssh` and `600` for `authorized_keys`.
- Use `BatchMode=yes` for automated tests so failures do not hang waiting for a password.
- Before deployment, confirm `docker ps` or other service checks will not affect unrelated containers or processes.

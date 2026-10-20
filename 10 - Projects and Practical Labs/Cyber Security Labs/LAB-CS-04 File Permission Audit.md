---
title: "File Permission Audit"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "LAB-CS-04"
type: "lab"
difficulty: "foundation"
status: "not-started"
mastery: 0
prerequisites:
  - "[[CS-10 Operating System Security and Hardening]]"
tags:
  - semester-6
  - cyber-security
  - lab
---

# LAB-CS-04 File Permission Audit

> [!danger] Ethics and scope
> The script creates its own deliberately misconfigured practice directory. The read-only `--audit-only` mode may be pointed only at directories **you own** (e.g. your own project folder). Don't audit shared servers or other users' files without the administrator's permission.

**Script:** `scripts/lab04_permissions.py` · **Tests:** `tests/test_labs.py::test_lab04` (passing, using a temporary directory) · **Time:** 45–60 min · **Platform:** Linux, macOS or WSL (POSIX permissions) · **Related lessons:** [[CS-10 Operating System Security and Hardening]], [[CS-04 Authorization and Access Control]]

## Objectives
1. Read permission modes in octal and symbolic form, including setuid and sticky bits.
2. Detect world-writable files and directories, setuid binaries, secrets readable by others, and executable data files.
3. Apply least-privilege fixes and confirm them with a re-audit.
4. Compare the script's findings with standard `ls` and `find` commands.

## Prerequisites
- Python 3.10+ on a POSIX system.
- CS-10 §5.2.

## Setup
```bash
cd "10 - Projects and Practical Labs/Cyber Security Labs"
umask          # note your current umask (often 0022)
```

## Procedure (commands)
1. Create the practice workspace, audit it, fix it, and re-audit: `python scripts/lab04_permissions.py`
2. Before step 2's fixes are applied, the workspace contains these deliberate mistakes:

   | Path | Mode | Problem |
   |---|---|---|
   | `app/.env` | 644 | A secret readable by everyone |
   | `app/notes.txt` | 755 | A data file marked executable |
   | `uploads/` | 777 | A world-writable directory |
   | `shared_tmp/` | 1777 | World-writable **with sticky bit** (like `/tmp`); acceptable |
   | `backup.sh` | 777 | A script anyone can modify |
   | `tools/report_tool` | 4755 | setuid |

3. Re-create the broken state and inspect it with standard tools:
   ```bash
   python scripts/lab04_permissions.py --cleanup
   python -c "import sys; sys.path.insert(0,'scripts'); import lab04_permissions as l; from pathlib import Path; l.setup(Path('lab04_workspace'))"
   ls -la lab04_workspace lab04_workspace/app lab04_workspace/tools
   find lab04_workspace -perm -0002 ! -type l          # world-writable entries
   find lab04_workspace -perm -4000 -type f            # setuid files
   ```
4. Fix them by hand with `chmod`, and confirm with `python scripts/lab04_permissions.py --audit-only lab04_workspace`.
5. Optional, read-only: audit one of **your own** project folders with `--audit-only`.

## Expected output
Real output from the build machine (Linux):
```text
== Step 1: audit the deliberately misconfigured workspace ==
HIGH   secret readable/writable by group or others (want 600)  rw-r--r--  644 app/.env
HIGH   setuid bit                                              rwsr-xr-x 4755 tools/report_tool
HIGH   world-writable                                          rwxrwxrwx  777 backup.sh
HIGH   world-writable                                          rwxrwxrwx  777 uploads
LOW    data file marked executable                             rwxr-xr-x  755 app/notes.txt

== Step 2: apply least-privilege fixes ==
chmod  600 app/.env
chmod  644 app/notes.txt
chmod  750 uploads
chmod  700 backup.sh
chmod  755 tools/report_tool

== Step 3: re-audit ==
no findings
```
`find … -perm -0002` will also list `shared_tmp`, because `find` doesn't treat the sticky bit as an exception. The script deliberately doesn't flag it (see Interpretation).

## Interpretation
- **`app/.env` 644:** any local user can read the app's secrets, so it's fixed to 600 (owner only).
- **`backup.sh` 777:** if root or a cron job runs this script, any user can insert commands that run with those privileges (CS-10 Example 3). It's fixed to 700, and it should be owned by the account that runs it.
- **`uploads/` 777:** anyone can add, replace or delete files, which allows planting content or deleting others' uploads. 750 gives the owner full control and the group read access.
- **`tools/report_tool` 4755:** setuid runs the program as its owner. Unless it's essential and carefully written, remove the bit.
- **`shared_tmp/` 1777:** world-writable, but the sticky bit means users can delete only their own files, the standard design for shared temporary directories. It's still worth asking whether a shared directory is needed at all.
- **`app/notes.txt` 755:** low risk, but executable data files are sloppy and sometimes exploitable. Fixed to 644.

## Cleanup
```bash
python scripts/lab04_permissions.py --cleanup
```
This deletes the directory only if it contains the `.lab04` marker file.

## Questions
1. Write the octal mode for `rwxr-x---` and for `rw-r-----`.
2. Why is a world-writable script dangerous even if the file's owner is an ordinary user?
3. What does the sticky bit change for a world-writable directory?
4. Your web server runs as `www-data` and must read (not write) `app/config.yml`, which is owned by `deploy`. Propose an owner, group and mode.
5. Why does the script use `os.lstat` and skip symbolic links?

## Answers
> [!success]- Answers
> 1. `rwxr-x---` = 750; `rw-r-----` = 640.
> 2. Whoever *runs* the script executes the attacker's changes with the runner's privileges. If an administrator, a scheduled job or another user runs it, the attacker gains their rights. Writeability by others breaks the link between "who controls the code" and "who runs it".
> 3. Without it, any user with write access to the directory can delete or rename any file in it. With it, only the file's owner (or the directory's owner, or root) can delete or rename it.
> 4. Owner `deploy`, group `www-data`, mode **640**: deploy can edit it, the web server can read it, others get nothing. The web server can't modify its own configuration.
> 5. Following a symlink could make the audit report on files outside the audited tree (or loop forever). `lstat` inspects the link itself, so the audit stays inside the tree you meant to scan.

## Defensive lessons
- Secrets: 600 (or 640 with a dedicated group), owned by the service account.
- Nothing executed by privileged accounts should be writeable by less-privileged users, including the parent directories.
- Avoid 777; find who needs which access and grant only that.
- Review setuid/setgid binaries against a known-good list.
- Automate the audit and re-run it after deployments.

## Mastery checklist
- [ ] I can explain every finding in the expected output
- [ ] I fixed the workspace by hand and got "no findings"
- [ ] I compared the findings with `ls -la` and `find -perm`
- [ ] I cleaned up

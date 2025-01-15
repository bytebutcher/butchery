# Git Toolkit

## git-auto-commit

A simple daemon/script that automatically commits and pushes changes in a Git repository based on a specified time frame.

### ROADMAP

- allow passing a csv file containing a list of repo-paths (and timeframes)
- allow passing a list of repo-paths
- allow specifying how often the daemon checks the repo-path in a given timeframe (or autocompute based on given timeframe)

### Usage

```bash
./git-auto-commit -r <repository_path> -t <timeframe_hours> [-d]
```

### Examples

```
# Run once
./git-auto-commit -r /path/to/repo -t 24

# Run as daemon
./git-auto-commit -r /path/to/repo -t 24 -d
```

### Setup

**General setup:**

- Copy script to `/usr/local/bin`:
```
sudo cp git-auto-commit /usr/local/bin/
sudo chmod +x /usr/local/bin/git-auto-commit
```

- Run once, setup as cronjob or run as daemon (see below)

**Cronjob setup:**

Add this line to your crontab to check hourly whether the repository was commited at least once a day:
```
0 * * * * /usr/local/bin/git-auto-commit -r /path/to/repo -t 24 2>&1
```

**Daemon setup:**

- Copy the service file. 
```
sudo cp git-auto-commit.service /etc/systemd/system/
```

- Adjust the username and repository path


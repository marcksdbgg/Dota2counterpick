# core — Resumen de Codebase

## Estructura (hasta 2 niveles)

```
tmpgzmf4ivp/
├── dev
│   ├── archiveTest.mts
│   ├── axios.mts
│   ├── checkAccounts.ts
│   ├── convertSpec.ts
│   ├── copyUsage.ts
│   ├── deleteTest.ts
│   ├── findProMatches.mts
│   ├── fixProMatches.mts
│   ├── generateFakeRatings.mts
│   ├── keyTest.mts
│   ├── legacyArchive.ts
│   ├── lobby.ts
│   ├── metaParse.mts
│   ├── minRetriever.ts
│   ├── playerCachesArchive.mts
│   ├── reParse.ts
│   ├── repatch.ts
│   ├── teamElo.ts
│   ├── teamMatch.mts
│   ├── transferGcData.mts
│   ├── updateProtos.mts
│   └── wordcount.ts
├── elasticsearch
│   ├── elasticsearch-index.sh
│   └── index.json
├── fetcher
│   ├── base.ts
│   ├── getApiData.ts
│   ├── getArchivedData.ts
│   ├── getGcData.ts
│   ├── getMeta.ts
│   └── getParsedData.ts
├── json
│   ├── 1781962623_api.json
│   ├── 1781962623_gcdata.json
│   ├── 1781962623_identity.json
│   ├── 1781962623_output.json
│   ├── 1781962623_parsed.json
│   ├── 1781962623_playercache_api_0.json
│   ├── 1781962623_playercache_gcdata_0.json
│   ├── 1781962623_playercache_parsed_0.json
│   ├── 3254426673_api.json
│   ├── 3254426673_output.json
│   ├── 3254426673_playercache_api_0.json
│   ├── 7468445438_meta.json
│   ├── 7490235544_api.json
│   ├── 7490235544_gcdata.json
│   ├── 7490235544_identity.json
│   ├── 7490235544_parsed.json
│   ├── 7490235544_playercache_api_0.json
│   ├── 7490235544_playercache_gcdata_0.json
│   └── 7490235544_playercache_parsed_0.json
├── proto
│   ├── base_gcmessages.proto
│   ├── c_peer2peer_netmessages.proto
│   ├── clientmessages.proto
│   ├── connectionless_netmessages.proto
│   ├── demo.proto
│   ├── dota_broadcastmessages.proto
│   ├── dota_client_enums.proto
│   ├── dota_clientmessages.proto
│   ├── dota_commonmessages.proto
│   ├── dota_fighting_game_p2p_messages.proto
│   ├── dota_gcmessages_client.proto
│   ├── dota_gcmessages_client_battle_report.proto
│   ├── dota_gcmessages_client_bingo.proto
│   ├── dota_gcmessages_client_candy_shop.proto
│   ├── dota_gcmessages_client_chat.proto
│   ├── dota_gcmessages_client_coaching.proto
│   ├── dota_gcmessages_client_fantasy.proto
│   ├── dota_gcmessages_client_guild.proto
│   ├── dota_gcmessages_client_guild_events.proto
│   ├── dota_gcmessages_client_match_management.proto
│   ├── dota_gcmessages_client_showcase.proto
│   ├── dota_gcmessages_client_team.proto
│   ├── dota_gcmessages_client_tournament.proto
│   ├── dota_gcmessages_client_watch.proto
│   ├── dota_gcmessages_common.proto
│   ├── dota_gcmessages_common_bot_script.proto
│   ├── dota_gcmessages_common_fighting_game.proto
│   ├── dota_gcmessages_common_league.proto
│   ├── dota_gcmessages_common_lobby.proto
│   ├── dota_gcmessages_common_match_management.proto
│   ├── dota_gcmessages_common_overworld.proto
│   ├── dota_gcmessages_common_survivors.proto
│   ├── dota_gcmessages_msgid.proto
│   ├── dota_gcmessages_server.proto
│   ├── dota_gcmessages_webapi.proto
│   ├── dota_hud_types.proto
│   ├── dota_match_metadata.proto
│   ├── dota_messages_mlbot.proto
│   ├── dota_modifiers.proto
│   ├── dota_scenariomessages.proto
│   ├── dota_shared_enums.proto
│   ├── dota_usercmd.proto
│   ├── dota_usermessages.proto
│   ├── econ_gcmessages.proto
│   ├── econ_shared_enums.proto
│   ├── engine_gcmessages.proto
│   ├── enums_clientserver.proto
│   ├── gameevents.proto
│   ├── gametoolevents.proto
│   ├── gcsdk_gcmessages.proto
│   ├── gcsystemmsgs.proto
│   ├── netmessages.proto
│   ├── network_connection.proto
│   ├── networkbasetypes.proto
│   ├── networksystem_protomessages.proto
│   ├── steamdatagram_messages_auth.proto
│   ├── steamdatagram_messages_sdr.proto
│   ├── steammessages.proto
│   ├── steammessages_base.proto
│   ├── steammessages_clientserver_login.proto
│   ├── steammessages_cloud.steamworkssdk.proto
│   ├── steammessages_gamenetworkingui.proto
│   ├── steammessages_helprequest.steamworkssdk.proto
│   ├── steammessages_int.proto
│   ├── steammessages_oauth.steamworkssdk.proto
│   ├── steammessages_player.steamworkssdk.proto
│   ├── steammessages_publishedfile.steamworkssdk.proto
│   ├── steammessages_steamlearn.steamworkssdk.proto
│   ├── steammessages_unified_base.steamworkssdk.proto
│   ├── steamnetworkingsockets_messages.proto
│   ├── steamnetworkingsockets_messages_certs.proto
│   ├── steamnetworkingsockets_messages_udp.proto
│   ├── te.proto
│   ├── uifontfile_format.proto
│   ├── usercmd.proto
│   ├── usermessages.proto
│   └── valveextensions.proto
├── routes
│   ├── requests
│   ├── responses
│   ├── api.ts
│   ├── generateOperationId.ts
│   ├── keyManagement.ts
│   ├── playerFields.ts
│   ├── README_FOR_API_KEYS.md
│   └── spec.ts
├── scripts
│   ├── backend.sh
│   ├── benchmark.sh
│   ├── cassandra.sh
│   ├── cycler.py
│   ├── cycler_old.py
│   ├── deploy.sh
│   ├── elasticsearch.sh
│   ├── fullhistory.sh
│   ├── gce.sh
│   ├── launch.sh
│   ├── parser.sh
│   ├── parser_external.sh
│   ├── postgres.sh
│   ├── proxy.sh
│   ├── redis.sh
│   ├── request.sh
│   ├── retriever.sh
│   ├── retriever_external.sh
│   ├── retriever_mig.sh
│   ├── scw.sh
│   ├── scylla.sh
│   ├── test.sh
│   ├── wait-cassandra.sh
│   └── web.sh
├── sql
│   ├── cachehit.sql
│   ├── colsize.sql
│   ├── country_mmr.sql
│   ├── create_tables.cql
│   ├── create_tables.sql
│   ├── currentmmr.sql
│   ├── dbsize.sql
│   ├── game_mode.sql
│   ├── init.cql
│   ├── init.sql
│   ├── leaderboard.sql
│   ├── lobby_type.sql
│   ├── longrunning.sql
│   ├── metric_lasthit.sql
│   ├── migrations.cql
│   ├── migrations.sql
│   ├── mmr.sql
│   ├── mmrestimate.sql
│   ├── ranking.sql
│   ├── ranks.sql
│   └── rowsize.sql
├── store
│   ├── archive.ts
│   ├── cassandra.ts
│   ├── db.ts
│   ├── elasticsearch.ts
│   ├── queue.ts
│   ├── redis.ts
│   ├── search.ts
│   ├── searchES.ts
│   └── stripe.ts
├── svc
│   ├── apiadmin.ts
│   ├── archiver.ts
│   ├── autocache.ts
│   ├── autofullhistory.ts
│   ├── backfill.ts
│   ├── backupscanner.ts
│   ├── buildsets.ts
│   ├── cleanup.ts
│   ├── cosmetics.ts
│   ├── counts.ts
│   ├── cycler.ts
│   ├── distributions.ts
│   ├── fullhistory.ts
│   ├── gcdata.ts
│   ├── heroes.ts
│   ├── items.ts
│   ├── leagues.ts
│   ├── livegames.ts
│   ├── migrater.ts
│   ├── mmr.ts
│   ├── monitor.ts
│   ├── parser.ts
│   ├── profiler.ts
│   ├── proplayers.ts
│   ├── proxy.ts
│   ├── reconcile.ts
│   ├── retriever.ts
│   ├── scanner.ts
│   ├── scenarios.ts
│   ├── syncSubs.ts
│   ├── teams.ts
│   └── web.ts
├── util
│   ├── archiveUtil.ts
│   ├── benchmarksUtil.ts
│   ├── buildMatch.ts
│   ├── buildPlayer.ts
│   ├── buildStatus.ts
│   ├── compute.ts
│   ├── filter.ts
│   ├── insert.ts
│   ├── laneMappings.ts
│   ├── pgroup.ts
│   ├── playerCaches.ts
│   ├── queries.ts
│   ├── scenariosUtil.ts
│   ├── types.ts
│   └── utility.ts
├── .env_example
├── .gitattributes
├── .gitignore
├── .prettierignore
├── CODE_OF_CONDUCT.md
├── config.ts
├── CONTRIBUTORS.js
├── docker-compose.override.yml
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.retriever
├── ecosystem.config.js
├── eslint.config.js
├── global.d.ts
├── index.ts
├── LICENSE
├── package-lock.json
├── package.json
├── README.md
└── tsconfig.json
```

### `CODE_OF_CONDUCT.md`
```md
# Contributor Covenant Code of Conduct

## Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, sex characteristics, gender identity and expression,
level of experience, education, socio-economic status, nationality, personal
appearance, race, religion, or sexual identity and orientation.

## Our Standards

Examples of behavior that contributes to creating a positive environment
include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexualized language or imagery and unwelcome sexual attention or
  advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as a physical or electronic
  address, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

## Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at support@opendota.com. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at https://www.contributor-covenant.org/version/1/4/code-of-conduct.html

[homepage]: https://www.contributor-covenant.org

For answers to common questions about this code of conduct, see
https://www.contributor-covenant.org/faq

```

### `README.md`
```md
# opendota-core

[![Help Contribute to Open Source](https://www.codetriage.com/odota/core/badges/users.svg)](https://www.codetriage.com/odota/core)

## Overview

- This project provides the [OpenDota API](https://docs.opendota.com/) for consumption.
- This API powers the [OpenDota UI](https://www.opendota.com), which is also an [open source project](https://github.com/odota/ui).
- Raw data comes from the WebAPI provided by Valve and fully automated parsing of match replays (.dem files).
- A public deployment of this code is maintained by The OpenDota Project.

## Tech Stack

- Microservices: Node.js
- Databases: PostgreSQL/Redis/Cassandra
- Parser: Java (powered by [clarity](https://github.com/skadistats/clarity))

## Quickstart (Docker)

- Install Docker: `curl -sSL https://get.docker.com/ | sh`. If you are on Windows, make sure you shared the working drive with Docker.
- Install Docker Compose: `curl -L "https://github.com/docker/compose/releases/download/1.17.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose`. If you are on Windows, docker-compose comes with the msi package.
- Create .env file with required config values in KEY=VALUE format (see config.js for a full listing of options) `cp .env_example .env`
  - `STEAM_API_KEY` You need this in order to access the Steam Web API, which is used to fetch basic match data and player profile data. You can use your main account to obtain the API key; it does not have to match the account used for the `STEAM_USER` and `STEAM_PASS` options. You can request an API key here: https://steamcommunity.com/dev/apikey
  - `STEAM_USER, STEAM_PASS` A Steam account is required to fetch replay salts. It is recommended to use a new account for this purpose (you won't be able to use the account on two different hosts at the same time, and the account must not have Steam Guard enabled). This is not required if you don't need to download/parse replays.
- Start containers and initialize databases: `docker-compose up`
- Make some changes and commit them.
- Submit a pull request. Wait for it to be reviewed and merged.
- **OPTIONAL** Add your DOTA friend code (SteamId3) to the `CONTRIBUTORS.js` file.
- Congratulations! You're a contributor.

## Notes

- The API runs on port 5000 by default.
- File changes made in the host directory get mirrored into the container.
- Get a terminal into the running container: `docker exec -it odota-core bash`
- The process manager `pm2` is used to manage the individual services. Each is run as a separate Node.js process. By default, only the web service is launched.
  - `pm2 list` See the currently running services.
  - `pm2 start ecosystem.config.js` Start all the services
  - `pm2 start ecosystem.config.js --only web` Starts a specific service
  - `pm2 stop web` Stop a specific service
  - `pm2 stop all` Stop all the services
  - `pm2 logs web` Inspect the output of a service
  - `pm2 kill` Stop pm2 and all the processes if things are stuck
- `docker system prune` Cleans your system of any stopped containers, images, and volumes
- `docker-compose build` Rebuilds your containers (e.g. for database schema updates)
- `docker pull odota/parser` You may need to do this if the Java parse server has updated. Remove and recreate the parser container to run the latest code.
- Tests are written using the `mocha` framework.
  - `npm test` runs the full test suite.
  - Use `mocha` CLI for more fine-grained control over the tests you want to run.
- Starter data
  - You can request a parse by ID to get a match with parsed data, e.g. `npm run request`
    - To complete a parse the following services need to be running: `pm2 start ecosystem.config.js --only web,retriever,parser`
  - Or request a match history refresh on a player to get up to 500 of their recent matches, e.g. `npm run fullhistory`
    - This requires the fullhistory service: `pm2 start ecosystem.config.js --only fullhistory`

## Resources

- Join us on Discord (https://discord.gg/opendota)! We're always happy to help and answer questions.
- The following blog posts may help you understand the codebase/architecture:
  - General Learnings: https://odota.github.io/blog/2016/05/13/learnings/
  - Architecture: https://odota.github.io/blog/2016/05/15/architecture/
  - Deployment/Infrastructure: https://odota.github.io/blog/2016/08/10/deployment/

## History

- Project started in August 2014
- Forked from https://github.com/RJacksonm1/matchurls

```

### `routes/README_FOR_API_KEYS.md`
```md
Make sure to set these ENV variables:

STEAM_API_KEY=
STRIPE_SECRET=
STRIPE_API_PLAN=
UI_HOST=http://localhost:3000
ENABLE_API_LIMIT=true
API_BILLING_UNIT=1

```

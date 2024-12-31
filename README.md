
<h1 align="center">
  Savage Aim
  <br>
</h1>

<h4 align="center">A Best-in-Slot manager for you and your Final Fantasy XIV raid team!</h4>

<p align="center">
  <a href="https://github.com/SavageAim/app/releases/latest" target="_blank">
    <img src="https://img.shields.io/github/v/release/SavageAim/app" alt="Latest Release" />
  </a>
  <a href="https://wiki.savageaim.com" target="_blank">
    <img alt="Wiki" src="https://img.shields.io/badge/GitBook-wiki-blue?logo=gitbook">
  </a>
</p>

## Key Features
- Track your own Best-in-Slot lists for multiple Jobs, with available importing from Etro or XIVGear!
- Create Teams to track the gearing requirements/progress of everyone in your raid team!
- Access Loot Tracking systems that automatically update your Team Member's BIS information when they recieve drops!
- Also access a solver for optimising loot handouts in the fairest way to get you finished with a fight ASAP!
- And if your friends don't want to join the site, make proxies for all their characters to still get all of these features!

## How To Use
Sign up using your Discord account on https://savageaim.com and go from there!
If you have any issues or questions, feel free to join the Discord from the link on the footer of the site, or open an issue here!

## Related
[Savage Aim Dalamud Plugin](https://github.com/SavageAim/plugin) - Dalamud Plugin for updating your BIS Lists from in-game, if you use those sorts of things

## Development
Running SavageAim locally for development has a few steps but is relatively straightforward;

### Requirements
- Docker installed, preferably a version that comes with `compose` though for older versions `docker-compose` can be installed separately.
- Python 3.8 or higher, and pip
- NodeJS 16.x

### Instructions
1. Clone the repo
2. In the root directory, run `docker compose up -d` to set up the service containers for *redis*, *postgres*, and *nginx* as a load balancer
3. Backend setup, skip these steps if you have already run the backend before
   1. Navigate to `backend` and run `pip3 install -r requirements.txt` to install the requirements. Feel free to create a virtualenv in advance if you wish!
   2. Run `python3 manage.py migrate` to apply migrations to the postgres container. Postgres data is saved under `database-data` in the top level directory.
   3. Run `python3 manage.py seed` to populate the DB with all of the Gear, Tier, and other constant information.
   3. Run `python3 manage.py dev_setup` to set up the local site for you to be able to log in and use.
4. Run `python3 manage.py runserver 0.0.0.0:8000` to bring up a development server for the backend. Leave this terminal tab running this command to leave the dev backend running.
5. In a separate terminal tab/window, navigate to the `frontend` directory. Run `npm install` if you haven't previously.
6. Run `npm run serve` to bring up a development frontend.
7. Visit `localhost:8080` in your browser to view the site locally. This port actually accesses the *nginx* container to ensure requests are routed properly between the front and backends.

### Usage
To log in and start using the site, you will need to visit `localhost:8080/backend/admin` and log in using the form on that page with username `devuser` and password `password`.
Once the login is successful, returning to `localhost:8080` will let you use the site as normal.

The devuser is set up with the following information;
- 2 Characters;
  - Character 1 is unverified, allowing you to see/interact with the site with an unverified character.
  - Character 2 is verified, allowing you to see/interact with the site with a verified character.
    - Character 2 also has 3 BIS Lists, one for each role, and has joined each Team with one of these, allowing vision of the Loot Solver Need/Greed setups for them in every Team.
- 3 Teams;
  - Team 1 is led by Character 2, and contains Character 3, a Character belonging to another user.
  - Team 2 is led by Character 3, with Character 2 as a Member with no permissions.
  - Team 3 is also led by Character 3, but Character 2 now has Loot Manager and Proxy Manager permissions.
  - All Teams also contain Character 4, a proxy Character.

If you wish to access Character 3's user to edit permissions of Character 2 in either Team, log out and then log in with `devuser2` instead to access that account.

Re-running the `python3 manage.py dev_setup` command will give you a message stating that the DB was already set up, and ask if you want to reset it.
This just means that if you change things and want a clean slate, just re-run the command and say yes.

If there are any issues with local development, please let me know either on Discord or as an Issue on the repo!


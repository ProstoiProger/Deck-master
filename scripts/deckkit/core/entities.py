"""Character images for the Minecraft-style themes (Steve, Creeper and friends).

The images are NOT shipped with the skill. `fetch` downloads Mojang's public MHF skin heads through the community
render services minotar.net and mc-heads.net into assets/entities (git-ignored), for personal, non-commercial decks
(see references/design/entities.md for the usage rules). Layouts look entities up by name and fall back to an
initials badge when an image is missing.

Kinds: `face` flat head (256 px), `head` isometric 3D head with transparency, `body` full figure (Steve and Alex).
"""
import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path

from .paths import ROOT

UA = "deck-master/1.0 (personal presentation assets)"
SERVICES = {"face": "https://minotar.net/avatar/{mhf}/256.png", "head": "https://mc-heads.net/head/{mhf}/256",
            "body": "https://mc-heads.net/body/{mhf}/256"}

# name -> (Mojang MHF account, label, suggested role in a deck, group)
# groups: player, friendly, hostile, block. Groups pick the decoration pools of the game themes.
ENTITIES = {
    # players
    "steve": ("MHF_Steve", "Steve", "default team member", "player"),
    "alex": ("MHF_Alex", "Alex", "team member", "player"),
    # friendly and neutral
    "villager": ("MHF_Villager", "Villager", "domain expert, trader, mentor", "friendly"),
    "pig": ("MHF_Pig", "Pig", "friendly mascot, test user", "friendly"),
    "cow": ("MHF_Cow", "Cow", "resource, data source", "friendly"),
    "mooshroom": ("MHF_MushroomCow", "Mooshroom", "rare resource, special case", "friendly"),
    "chicken": ("MHF_Chicken", "Chicken", "small helper, microservice", "friendly"),
    "sheep": ("MHF_Sheep", "Sheep", "users, crowd, followers", "friendly"),
    "wolf": ("MHF_Wolf", "Wolf", "loyal helper, monitoring", "friendly"),
    "cat": ("MHF_Cat", "Cat", "curious user, small helper", "friendly"),
    "ocelot": ("MHF_Ocelot", "Ocelot", "scout, fast explorer", "friendly"),
    "horse": ("MHF_Horse", "Horse", "transport, throughput, delivery", "friendly"),
    "fox": ("MHF_Fox", "Fox", "clever shortcut, smart trick", "friendly"),
    "panda": ("MHF_Panda", "Panda", "calm, stable service", "friendly"),
    "parrot": ("MHF_Parrot", "Parrot", "echo, notifications, messaging", "friendly"),
    "bee": ("MHF_Bee", "Bee", "workers, parallel jobs, workers", "friendly"),
    "rabbit": ("MHF_Rabbit", "Rabbit", "fast, quick win", "friendly"),
    "turtle": ("MHF_Turtle", "Turtle", "slow but steady, long-running job", "friendly"),
    "dolphin": ("MHF_Dolphin", "Dolphin", "smart helper, guide", "friendly"),
    "squid": ("MHF_Squid", "Squid", "ink, logs, cloud", "friendly"),
    "goat": ("MHF_Goat", "Goat", "peak performance, climbing metrics", "friendly"),
    "allay": ("MHF_Allay", "Allay", "assistant, collects items, helper bot", "friendly"),
    "sniffer": ("MHF_Sniffer", "Sniffer", "discovery, search, finding seeds", "friendly"),
    "iron-golem": ("MHF_Golem", "Iron Golem", "guard, security, protection", "friendly"),
    # hostile
    "creeper": ("MHF_Creeper", "Creeper", "risk, bug, sudden failure", "hostile"),
    "zombie": ("MHF_Zombie", "Zombie", "legacy system, backlog, tech debt", "hostile"),
    "skeleton": ("MHF_Skeleton", "Skeleton", "attacker, adversary, edge case", "hostile"),
    "stray": ("MHF_Stray", "Stray", "cold start, frozen job", "hostile"),
    "husk": ("MHF_Husk", "Husk", "drought, dry data, burnt-out", "hostile"),
    "drowned": ("MHF_Drowned", "Drowned", "flooded queue, overload", "hostile"),
    "spider": ("MHF_Spider", "Spider", "crawler, scraper, network", "hostile"),
    "cave-spider": ("MHF_CaveSpider", "Cave Spider", "small bug, poison, hidden defect", "hostile"),
    "enderman": ("MHF_Enderman", "Enderman", "teleporting data, migration, sync", "hostile"),
    "endermite": ("MHF_Endermite", "Endermite", "tiny leak, side effect", "hostile"),
    "silverfish": ("MHF_Silverfish", "Silverfish", "pests hiding in stone, hidden infestation", "hostile"),
    "blaze": ("MHF_Blaze", "Blaze", "load, heat, performance pressure", "hostile"),
    "ghast": ("MHF_Ghast", "Ghast", "big threat, outage", "hostile"),
    "magma-cube": ("MHF_LavaSlime", "Magma Cube", "bouncing hot issue, cascading failure", "hostile"),
    "slime": ("MHF_Slime", "Slime", "memory leak, splitting tasks", "hostile"),
    "witch": ("MHF_Witch", "Witch", "magic, black box, ML model", "hostile"),
    "phantom": ("MHF_Phantom", "Phantom", "night shift, insomnia, on-call", "hostile"),
    "vex": ("MHF_Vex", "Vex", "annoying alerts, noise", "hostile"),
    "evoker": ("MHF_Evoker", "Evoker", "summoner, orchestrator, spawner", "hostile"),
    "vindicator": ("MHF_Vindicator", "Vindicator", "hard rule enforcer, strict policy", "hostile"),
    "pillager": ("MHF_Pillager", "Pillager", "raider, data theft, resource drain", "hostile"),
    "guardian": ("MHF_Guardian", "Guardian", "sentinel, monitoring beam", "hostile"),
    "warden": ("MHF_Warden", "Warden", "ultimate security, audit, strict compliance", "hostile"),
    "shulker": ("MHF_Shulker", "Shulker", "storage box, hidden container", "hostile"),
    "piglin": ("MHF_Piglin", "Piglin", "trader, gold, budget", "hostile"),
    "zombified-piglin": ("MHF_PigZombie", "Zombified Piglin", "old system with gold, costly legacy", "hostile"),
    "strider": ("MHF_Strider", "Strider", "walks on lava, handles hot paths", "hostile"),
    "pufferfish": ("MHF_Pufferfish", "Pufferfish", "defensive spike, rate limit", "hostile"),
    # blocks and signs
    "tnt": ("MHF_TNT", "TNT", "explosive growth, breaking change", "block"),
    "chest": ("MHF_Chest", "Chest", "storage, database, loot, results", "block"),
    "cake": ("MHF_Cake", "Cake", "reward, success, release", "block"),
    "pumpkin": ("MHF_Pumpkin", "Pumpkin", "seasonal event, harvest", "block"),
    "melon": ("MHF_Melon", "Melon", "fresh data, growth", "block"),
    "cactus": ("MHF_Cactus", "Cactus", "defensive, thorny edge case", "block"),
    "oak-log": ("MHF_OakLog", "Oak Log", "raw material, base layer", "block"),
    "question": ("MHF_Question", "Question sign", "questions, unknown, Q and A", "block"),
    "exclamation": ("MHF_Exclamation", "Exclamation sign", "warning, key point", "block"),
}
ALIASES = {"golem": "iron-golem", "iron_golem": "iron-golem", "irongolem": "iron-golem", "villagers": "villager", "magma": "magma-cube",
           "lavaslime": "magma-cube", "mushroom-cow": "mooshroom", "pigzombie": "zombified-piglin", "log": "oak-log"}
BODY_ONLY = {"steve", "alex"}
PROBE = "MHF_NoSuchAccountDeckMaster"  # used to learn what a service returns for unknown accounts


def entities_dir():
    override = os.environ.get("DECKKIT_ENTITIES_DIR")
    return Path(override) if override else ROOT / "assets" / "entities"


def canonical(name):
    n = str(name).strip().lower().replace(" ", "-")
    return ALIASES.get(n, n)


def known(name):
    return canonical(name) in ENTITIES


def find(name, kind="face"):
    """Path of the downloaded image or None."""
    n = canonical(name)
    suffix = "" if kind == "face" else f"-{kind}"
    p = entities_dir() / f"{n}{suffix}.png"
    return p if p.exists() else None


def group_of(name):
    return ENTITIES[canonical(name)][3]


def pool(group, available_only=True):
    """Entity names of a group; with available_only just those whose face image is downloaded."""
    names = [n for n, v in ENTITIES.items() if v[3] == group]
    return [n for n in names if find(n, "face")] if available_only else names


def status():
    """[(name, label, role, {kind: bool})] for every known entity."""
    rows = []
    for n, (_, label, role, _group) in ENTITIES.items():
        rows.append((n, label, role, {k: find(n, k) is not None for k in SERVICES}))
    return rows


def _download(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 (fixed https hosts above)
        data = r.read()
    if not data.startswith(b"\x89PNG"):
        raise ValueError("response is not a PNG")
    return data


def fetch(names=None, kinds=("face", "head", "body"), dest=None, force=False, opener=_download):
    """Download entity images. Returns (written, skipped, failed, unavailable): file names written, kept, failed
    (network or HTTP errors) and not offered by the service (the layouts then use the face image).
    `opener(url)` is injectable for tests. Existing files are kept unless force."""
    dest = Path(dest) if dest else entities_dir()
    dest.mkdir(parents=True, exist_ok=True)
    wanted = [canonical(n) for n in (names or ENTITIES)]
    unknown = [n for n in wanted if n not in ENTITIES]
    if unknown:
        raise ValueError(f"unknown entities {unknown}; choose from {sorted(ENTITIES)}")
    written, skipped, failed, unavailable, hashes, default_digest = [], [], [], [], {}, {}
    for n in wanted:
        mhf = ENTITIES[n][0]
        for kind in kinds:
            if kind == "body" and n not in BODY_ONLY:
                continue  # mob skins are heads on a black body; only the player skins make a useful figure
            fname = f"{n}.png" if kind == "face" else f"{n}-{kind}.png"
            target = dest / fname
            if target.exists() and not force:
                skipped.append(fname)
                continue
            try:
                data = opener(SERVICES[kind].format(mhf=mhf))
            except Exception as e:  # network, HTTP error or not a PNG
                failed.append(f"{fname}: {type(e).__name__}: {e}")
                continue
            digest = hashlib.sha256(data).hexdigest()[:12]
            if kind not in default_digest:  # what the service returns for an account that does not exist
                try:
                    default_digest[kind] = hashlib.sha256(opener(SERVICES[kind].format(mhf=PROBE))).hexdigest()[:12]
                except Exception:
                    default_digest[kind] = None
            if digest == default_digest[kind] and n != "steve":
                unavailable.append(f"{fname}: the service has no render for {mhf}; the face image is used instead")
                continue
            target.write_bytes(data)
            written.append(fname)
            hashes[fname] = digest
    manifest = dest / "manifest.json"
    old = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {"files": {}}
    old["files"].update(hashes)
    old.update({"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "sources": sorted(set(SERVICES.values())),
                "notice": "Minecraft characters belong to Mojang/Microsoft. Personal, non-commercial use only; "
                          "do not redistribute these files or imply endorsement. See references/design/entities.md."})
    manifest.write_text(json.dumps(old, indent=2), encoding="utf-8")
    return written, skipped, failed, unavailable

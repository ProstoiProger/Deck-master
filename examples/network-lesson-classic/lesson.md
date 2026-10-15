---
title: How a network sends a message
subtitle: Computer networks, opening lesson
event: assignment
theme: classic-craft
lang: en
minutes: 8
wpm: 140
max_slides: 12
team: Networks class
date: 2026-12-10
mobs: [pig, cow, sheep, chicken, wolf, fox, panda, bee, parrot, rabbit, villager, cat, horse, turtle, mooshroom, iron-golem]
sample: true            # illustrative lab numbers and fictional sources
---
# How a network sends a message
layout: title
eyebrow: Computer networks
mascot: pig
time: 20
notes: Welcome to the first lesson. In eight minutes we follow one chat message from your keyboard to another computer, through four layers, and we measure what it costs to deliver it reliably. Every slide uses a game picture, so you can remember the idea as an object you could hold.

---
# Hotbar: five stops on the message's trip
layout: agenda
time: 30
notes: Here are the five stops. The layers first, then how a packet is crafted, then the layers as the ground under a building, then the lab trade between two protocols, and finally the measured race. You can follow the animals along the hotbar.
- Layers | villager
- Packets | chicken
- Building | cow
- Protocols | fox
- Results | sheep

---
# Four layers fit in one backpack
layout: inventory
select: 2
source: inputs/lesson-notes.md
time: 50
notes: Think of the stack as a backpack with four slots. The application is the message itself. Transport splits it into segments and chooses TCP or UDP. The network layer picks the route by address. The link layer sends frames to the next device. The highlighted slot is the transport layer, which is where our lab happens. Counts show how many headers each layer adds to the message.
The slot you see highlighted is the layer our lab measures.
- Application | the message itself | book | 1
- Transport | splits it into segments | chest | 2
- Network | picks the route by address | torch | 3
- Link | sends frames to the next device | pickaxe | 4

---
# A packet is crafted from two headers and a piece of message
layout: crafting
result: Packet | chest | one piece of the message
source: inputs/lesson-notes.md
time: 50
notes: A packet is crafted like an item. One header with the sender and the receiver addresses, a second header with the sequence number, and a payload which is one piece of the message. Put them together and you get one packet that can travel on its own. The sequence number is how the other side puts the pieces back in order.
Three parts craft one packet that can travel alone.
- Header 1: addresses | book
- Header 2: sequence number | star
- Payload: a piece of the message | apple

---
# The layers are the ground under a building
layout: strata
source: inputs/lesson-notes.md
time: 45
notes: Another picture helps. The apps people see are the sky. Transport is the grass layer, the lobby that sorts the mail. Routing is the dirt, the corridors under the lobby. Links are the stone, the cables inside the walls. Each layer only talks to the layer next to it, like floors in a building.
- Application: Chat, Browser
- Transport: **TCP**, UDP
- Network: Router, Address
- Link: Cable, Switch

---
# Trade: TCP gives safety, UDP gives speed
layout: trade
trader: villager
source: inputs/lesson-notes.md
time: 55
notes: The lab showed a trade. TCP takes about eighteen milliseconds and loses nothing. UDP takes nine milliseconds but lost fourteen messages in a thousand. Pay with delay to get safety, or pay with safety to get speed. A villager would call both fair trades.
- 18 ms delay with TCP | 0 messages lost | the handshake and retries cost time
- 9 ms delay with UDP | 14 messages lost of 1,000 | nothing checks delivery

---
# Race: UDP is twice as fast as TCP
layout: leaderboard
better: lower
source: inputs/lesson-notes.md
time: 45
notes: Here is the race. Median delay in milliseconds, lower is better. UDP wins with nine, TCP finishes with eighteen. The gold trophy goes to the fastest, but remember that fast without delivery is not always a win.
- UDP | 9 ms | rabbit
- TCP | 18 ms | turtle

---
# Chat: the same conversation, segment by segment
layout: chat
source: inputs/lesson-notes.md
time: 50
notes: This is the conversation from the lab, as a chat. The client says hello in segment one, the server confirms it got segment one. Then the client asks for a file in segments two to five, and the server confirms it got all four. Those confirmations are what TCP does and UDP does not.
The lab conversation, one confirmation per segment.
- Client | hello server (segment 1) | cat
- Server | hello client, got segment 1 | villager
- Client | send me the file (segments 2 to 5) | cat
- Server | got segments 2 to 5 | villager

---
# Lab stats: TCP lost nothing, UDP lost 14 of 1,000
layout: hud
source: inputs/lesson-notes.md
time: 45
notes: Stats from the lab. TCP lost zero messages out of one thousand, so its health bar is full. UDP lost fourteen in a thousand, so its bar is almost full but not quite. UDP's median delay was nine milliseconds, half of TCP's eighteen. These were virtual machines, so real networks will vary.
- 0 of 1,000 | TCP messages lost | heart | every message arrived | 100
- 14 of 1,000 | UDP messages lost | hunger | no handshake, no retries | 98.6
- 9 ms | UDP median delay | xp | half of TCP's 18 ms | 50

---
# What we learned, and what we did not test
layout: book
source: inputs/lesson-notes.md
time: 45
notes: The left page is what we learned. Reliable delivery costs about twice the delay, and UDP lost fourteen messages of a thousand. The right page is honest limits. We used two virtual routers only, there was no wireless link, and a thousand messages is a small sample. Real networks vary.
## Learned
- Reliable delivery costs about twice the delay
- UDP lost 14 messages of 1,000
- Each layer talks only to its neighbour
## Not tested
- Wireless links
- More than two routers
- Larger samples than 1,000 messages

---
# Questions?
layout: closing
mascot: villager
achievement: Lesson complete
time: 15
notes: Thank you. In the lab you will repeat the measurement yourself on your own virtual machines.
- Lab guide: week 2 handout
- teacher@example.org

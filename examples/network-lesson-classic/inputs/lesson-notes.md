# Lesson notes: how a network sends a message (fictional, written by the teacher)

Class: first-year computer networks, 8-minute opening lesson, then a lab.

## Four layers (the stack)

- Application: the message itself, for example a chat line.
- Transport: splits the message into segments, TCP or UDP.
- Network: picks the route by address.
- Link: sends frames to the next device.

## Packet = envelope

A packet is a header plus a payload. Header 1: the sender and receiver addresses. Header 2: the sequence number.
Payload: a piece of the message. Put together they form one packet.

## Lab: 1,000 messages across three hops (two virtual routers)

| Protocol | Median delay (ms) | Messages lost of 1,000 | Setup |
|---|---|---|---|
| TCP | 18 | 0 | handshake |
| UDP | 9 | 14 | none |

Delay per hop with TCP: hop 1 6 ms, hop 2 5 ms, hop 3 7 ms.

## A message conversation in the lab

- Client says: "hello server" (segment 1).
- Server answers: "hello client, got segment 1".
- Client says: "send me the file" (segments 2 to 5).
- Server answers: "got segments 2 to 5".

## Where the layers live in a building analogy

Sky: apps people see. Grass: transport, the lobby that sorts the mail. Dirt: routing, the corridors. Stone: links, the cables in the walls.

## What we learned

- Reliable delivery costs about twice the delay (18 ms against 9 ms).
- UDP lost 14 messages of 1,000.
- Measured on virtual machines; real networks vary.

## Limits

- Two virtual routers only.
- No wireless link.
- Small sample: 1,000 messages.

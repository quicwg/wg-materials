# IETF 127: QUIC Working Group Session Minutes
**Date:** November 18, 2026
**Chairs:** Lucas Pardue, Matt Joras
**Note takers:** https://ietfminutes.org (AI generated and may contain mistakes)

## Summary
The QUIC Working Group met at IETF 127 to discuss working group drafts and proposals covering load balancing, qlog, receive timestamps, delegated stateless resets, congestion control data exchange, and peer-to-peer NAT traversal. Key highlights include QUIC-LB being prepared for Working Group Last Call (WGLC), a proposal to simplify qlog by removing TLS-specific layering violations, receive timestamps nearing WGLC, and strong support in the room for working on orphan connection resets caused by process crashes.

## Document Status Updates
*   **Multipath:**  RFC 10069 has been published!

## QUIC-LB: [QUIC-LB Update](https://datatracker.ietf.org/meeting/127/materials/slides-127-quic-quic-lb-update-00)
Martin Duke presented updates to `draft-ietf-quic-load-balancers`. QUIC-LB defines a structured connection ID (CID) format that allows layer-4 load balancers to route packets to the designated backend server without terminating connections. CIDs contain a Config ID (3 bits), a length self-encoding (5 bits), a Server ID, a Nonce, and optional extra bytes for server use. Three modes are defined: Plaintext, single-block AES-ECB (for a 16-byte Server ID + Nonce), and a four-pass Feistel cipher for variable-length encrypted CIDs.

*   **Deployment Status:** Plaintext mode is deployed in AWS NLB and Envoy. Encrypted QUIC-LB is being deployed by Google and another major vendor.
*   **Discussion:** Christian Huitema noted that the four-pass Feistel construction performs comparably to 64-bit block ciphers like Blowfish. Per Andersson recommended making the YANG module normative and requesting an early YANG Doctors review alongside the IANA registrations. Antonio Vicente asked about interest and motivation from hardware load balancer vendors.
*   **Next Steps:** The chairs proposed proceeding to WGLC alongside an early security review. The separate, expired Retry Offload draft will be retired due to lack of implementation interest.

## qlog: [qlog](https://datatracker.ietf.org/meeting/127/materials/slides-127-quic-qlog-00)
Lucas Pardue presented updates to `draft-ietf-quic-qlog-main-schema`, `draft-ietf-quic-qlog-quic-events`, and `draft-ietf-quic-qlog-h3-events`.

*   **TLS Layering Cleanup:** A proposal to remove TLS-specific fields and events (e.g., SNI, ALPN, cipher suite, resumption booleans) from the QUIC event schema, and move TLS logging into a separate TLS qlog extension draft. Christian Huitema volunteered to co-author it. Christian Huitema and Martin Duke supported the removal to keep protocol boundaries clean.
*   **Tuple and Path ID:** `tuple_id` will move to packet events only (`packet_sent`, `packet_received`, `packet_dropped`) rather than the generic event header. The core qlog documents will not add multipath events or path IDs. Yanmei Liu and Christian Huitema volunteered to work on a separate multipath qlog draft.
*   **`connection_id_updated` Event:** A proposal to delete this event, because it is redundant with packet headers and tuple assignment events.
*   **Discussion:** Participants generally supported simplifying the core qlog events to accelerate finalization.

## Receive Timestamps: [Receive timestamps](https://datatracker.ietf.org/meeting/127/materials/slides-127-quic-receive-timestamps-01)
Joseph Beshay presented updates to `draft-ietf-quic-receive-ts`. Changes include a range encoding change (`additional_timestamp_delta_count` starts at 0 for 1 delta), new transport parameter code points, explicit protocol violation error definitions, and decode safety bounds.

*   **Implementation Status:** Supported in MsQuic (v0.3/v0.4) and Google quiche (v0.4). Chrome deployment with BBR integration is planned for Q1.
*   **Discussion:** Magnus Westerlund requested clearer text on local microsecond clock assumptions and on interactions with ACK frequency. Yanmei Liu reported positive results from integrating receive timestamps into congestion controllers. The draft is nearing readiness for WGLC, pending minor text updates.

## SQUAD BoF Report: [SQUAD Report](https://datatracker.ietf.org/meeting/127/materials/slides-127-quic-squad-report-00)
Max Franke gave a brief readout of the SQUAD BoF held earlier in the week on multicast video delivery and QUIC abstractions. Key feedback was to broaden the focus from IP multicast to a general 1-to-many application interface abstraction over transport protocols. A dedicated mailing list will be created.

## Delegated Stateless Reset: [Delegated stateless resets](https://datatracker.ietf.org/meeting/127/materials/slides-127-quic-delegated-stateless-resets-00)
Stefano Duo presented `draft-kazuho-quic-delegated-stateless-reset`. The draft addresses orphan QUIC connections that occur when a user-space QUIC stack crashes or freezes while the host OS remains healthy. Without a normal teardown, these connections waste radio and battery resources. The proposal delegates stateless reset tokens to an OS or system component, using a new `RESET_TOKEN` frame and a server transport parameter.

*   **Discussion:** Rui Paulo, Ben Schwartz, Eric Kinnear, Ian Swett, and Lorenzo Colitti voiced strong support. They cited battery savings, user experience improvements, and OS API security boundaries: the OS can send stateless resets without granting applications raw packet generation.
*   **Session Poll:** "Should the working group work on a solution to this problem?" Yes: 35, No: 2, No Opinion: 8 (102 participants in session).

## Exchanging CC Data: [Exchanging CC data in QUIC](https://datatracker.ietf.org/meeting/127/materials/slides-127-quic-exchanging-cc-data-in-quic-00)
Jinghao Yuan presented `draft-yuan-quic-congestion-data`. The draft defines `CONGESTION_DATA` and `CONGESTION_DATA_RECALL` frames, along with transport parameters, to exchange congestion statistics (RTT, loss rate, bandwidth) between QUIC endpoints. It is used for adaptive bitrate (ABR) decisions and 0-RTT Careful Resume in TikTok live streaming. Production tests showed a 2.75% reduction in stall ratio and a 10.8% increase in bitrate.

*   **Discussion:** Lars Eggert questioned the potential harm or unfairness to competing flows at the bottleneck. Martin Duke, Antonio Vicente, and Nidhi Jaju suggested using `NEW_TOKEN` or SCONE mechanisms instead of exposing raw transport metrics to clients or JavaScript, citing cross-origin side-channel and fingerprinting risks. Kazuho Oku noted that server-to-client bandwidth hints are valuable for ABR logic.

## Cuback: [Cuback](https://datatracker.ietf.org/meeting/127/materials/slides-127-quic-cuback-00)
Kazuho Oku presented `draft-kazuho-ccwg-cuback`, an ACK-clocked formulation of Cubic. It replaces the window-tracking state machine with a pure `dW` function computed on entering recovery. This reduces implementation complexity and converges faster than standard Cubic with competing traffic. Detailed technical discussion will take place in CCWG / ICCRG.

## NAT Traversal: [QUIC NAT Traversal](https://datatracker.ietf.org/meeting/127/materials/slides-127-quic-quic-nat-traversal-00)
Marten Seemann presented `draft-seemann-quic-nat-traversal` and `draft-munizaga-quic-alternative-server-address`. The proposal builds peer-to-peer QUIC hole punching on MASQUE `CONNECT-UDP` relay channels and connection migration. An `ALTERNATIVE_ADDRESS` frame lets servers communicate candidate addresses after the handshake, so hole punching can run in the background without delaying connection setup.

*   **Discussion:** Aldi Sefa, Antonio Vicente, Nidhi Jaju, Eric Kinnear, Ben Schwartz, Stefano Duo, Marco Munizaga, Lorenzo Colitti, and Gorry Fairhurst discussed use cases (e.g., AirDrop, P2P file sharing), local network privacy implications, stateful firewalls versus NATs, and coordination across the IETF and W3C.

## Decisions and Action Items
*   **`draft-ietf-quic-load-balancers`:**
    *   **Action:** Chairs to issue WGLC, and to request an early security review and an early YANG Doctors review.
    *   **Action:** Retire the expired Retry Offload draft.
*   **qlog drafts** (`draft-ietf-quic-qlog-main-schema` / `draft-ietf-quic-qlog-quic-events` / `draft-ietf-quic-qlog-h3-events`):
    *   **Action:** qlog editors to remove TLS-specific fields and events, restrict `tuple_id` to packet events, and delete `connection_id_updated`. Proposals to be confirmed on GitHub and the mailing list.
    *   **Action:** TLS and multipath qlog definitions to be developed in separate documents.
*   **`draft-ietf-quic-receive-ts`:**
    *   **Action:** Authors to clarify clock precision assumptions before WGLC.
*   **Delegated Stateless Reset:**
    *   **Action:** The session poll showed strong support for working on the problem. Chairs to confirm interest and run any adoption call on the mailing list.

## Next Steps
*   Continue discussion of CC data exchange and P2P QUIC in the relevant venues (CCWG, ICCRG, MASQUE, QUIC).

## Note on Minute Generation

These minutes are sourced from the AI-generated summary published at https://ietfminutes.org/minutes/ietf127/quic.html, which notes the content is AI generated and may contain mistakes. The chairs verified the contents and made some minor changes before publishing the draft minutes. The WG may have proposed additional changes.

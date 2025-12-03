# IETF 124: QUIC Working Group Session Minutes
**Date:** November 6, 2025
**Chairs:** Lucas Pardue, Matt Joras
**Note takers:** Marco Munizaga
**Video Source:** [IETF 124: QUIC](https://www.youtube.com/watch?v=NIlCm62G0V8)


## Administrative & Updates
* **Re-charter:** The re-charter is complete, officially adding "QUIC Stream Multiplexing" as a fourth work area.
* **Document Status:** Three documents (Q-log, Multipath, Greasing) have passed Working Group Last Call and are awaiting shepherd write-ups.

## qlog
**Presenter:** Lucas Pardue
**Time:** [[07:57](http://www.youtube.com/watch?v=NIlCm62G0V8&t=477)]

* **Status Update:** An interim meeting resolved most blockers. There are 10 remaining open issues and 3 minor PRs.
* **Tooling:** Internal qlog tooling has been open-sourced, and `qvis` is receiving a significant update led by Robin Marx.
    * *Chat Context:* Robin Marx noted in chat that he has no plans to add major new features (like full multipath support) to `qvis` after this update, but the codebase will be easier for others to contribute to.
* **Scope Discussion:** The group debated whether to expand the scope to include "quick wins" (e.g., WebTransport’s `RESET_STREAM_AT` and Capsules) despite a 2022 decision to freeze scope.
    * **Lars Eggert & Marten Seemann:** Advocated for publishing the core document ASAP. They argued that if extensions are small (lines of code), they should just be merged to avoid delays, but larger work like Multipath qlog should remain separate.
    * **Christian Huitema:** Offered to work on the multipath extension but noted that updating tools to interpret multiple packet number spaces is the hard part.
* **Decision:** The editors will merge small, ready-to-go PRs (like `RESET_STREAM_AT`) even if it technically bends the previous scoping rule. This will be confirmed on the mailing list.

## QUIC Packet Received Timestamps
**Presenter:** Joseph Beshay
**Time:** [[25:37](http://www.youtube.com/watch?v=NIlCm62G0V8&t=1537)]

* **Design Issue:** The core debate was whether to make the extension independent of the ACK frame.
    * **The Conflict:** The draft proposes adding fields to the end of the existing ACK frame. This means the ACK frame is parsed differently depending on whether the timestamp Transport Parameter was negotiated.
    * **Christian Huitema:** Strongly opposed this, arguing that changing the parsing of an *existing* frame type based on negotiation is "dangerous" and a departure from QUIC v1 design principles.
    * **Kazuho Oku:** Countered that reusing the ID is correct to avoid a "combinatorial explosion" of frame IDs and running out of short IDs.
    * **Alessandro Ghedini:** Suggested a compromise where a separate Timestamp frame *must* immediately follow the ACK frame in the same packet to simplify parsing.
    * **Ted Hardie:** Emphasized that this is a fundamental design decision (parsing by frame type/version vs. transport parameter) rather than a "flip a coin" bike-shed issue.
* **Action Item:** Editors will take the design discussion back to the mailing list, specifically addressing the parsing strategy.

## QUIC Stream Multiplexing (QMUX)
**Presenter:** Kazuho Oku
**Time:** [[55:38](http://www.youtube.com/watch?v=NIlCm62G0V8&t=3338)]

* **Goal:** Provide a unified API for applications over different transport substrates (e.g., TCP+TLS vs. UDP+QUIC v1) to avoid redundant protocol development.
* **Proposal:** The "V-frames" approach—using QUIC v1 frame encodings directly on the byte stream.
* **Key Discussions:**
    * **Ossification (Ted Hardie):** Raised concerns that QMUX might ossify QUIC to a specific variant (QUIC v1 over TLS/TCP), potentially hindering future applications like Media over QUIC (MoQ) that require specific transport behaviors.
    * **Martin Duke:** Countered that MoQ over TCP is understood to be sub-optimal but QMUX doesn't change that equation; it essentially provides a fallback.
    * **Guillaume Hetier:** Expressed interest in QUIC over RDMA, suggesting QMUX should support broader use cases beyond just TLS over TCP.
    * **Chat Context:** Discussion on ALPN identifiers, with suggestions like "h3qmux" or "h3t" to distinguish from standard H3.
* **Poll Results:**
    * *Is this draft a suitable starting point for adoption?*
    * **Yes:** 29
    * **No:** 4
    * **No Opinion:** 21.
* **Action Item:** Chairs will confer with authors and the AD regarding the mixed interest and address the specific objections regarding negotiation and ossification.

## New Server Preferred Address
**Presenter:** Marko Munizaga
**Time:** [[01:42:54](http://www.youtube.com/watch?v=NIlCm62G0V8&t=6174)]

* **Proposal:** A `NEW_PREFERRED_ADDRESS` frame allowing a server to request a client migrate to a new address dynamically mid-connection.
* **Use Case:** Peer-to-peer contexts or MASQUE proxies where a server needs to migrate clients to a different proxy instance.
* **Discussion:**
    * **Christian Huitema:** Clarified that this is orthogonal to multipath; it works whether multipath is negotiated or not.
    * **Tommy Pauly:** Supported the work, noting it is valuable for peer-to-peer use cases.

## Exchanging Congestion Control Data
**Presenter:** Rich Salz
**Time:** [[01:53:35](http://www.youtube.com/watch?v=NIlCm62G0V8&t=6815)]

* **Proposal:** Two frames (`CONNECTION_CC_INFO`, `REQUEST_CC_DATA`) to exchange congestion control info, aiding "careful resume" when clients reconnect to different servers.
* **Status:** Currently in production use by TikTok.
* **Discussion:**
    * **Lars Eggert:** Noted similarities to the previous BDP frame discussion and questioned if CC data is comparable across different stacks.
    * **Security:** Concerns raised regarding sending this data in the clear (though integrity protected).

## Note on Minute Generation

These minutes synthesize the **official video recording**, **human-generated notes**, **AI-generated summary**, and the **live chat log**.


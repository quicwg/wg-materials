# IETF 126: QUIC Working Group Session Minutes
**Date:** July 22, 2026
**Chairs:** Lucas Pardue, Matt Joras
**Note takers:** https://ietfminutes.org (AI generated and may contain mistakes)

## Summary
The QUIC Working Group met at IETF 126 to discuss active working group drafts, potential new extensions, and operational telemetry. Key achievements include reliable stream resets entering working group last call (WGLC). Progress was reported across the QMux, Extended Key Update, Receive Timestamps, and qlog drafts, with several implementations maturing. The working group also heard several individual presentations covering zero-copy enhancements, Transport Services (TAPS) mapping gaps, alternative cryptographic suites, mutable idle timeouts, multicast integration, and peer-to-peer NAT traversal.

## Document Status Updates
*   **Chairs Presentation:** Reliable stream resets is in last call through August 3rd. Multiple drafts are awaiting shepherd write-ups. ([Chair slides](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-chair-slides-00))

## QMux: [QUIC-Aware Proxying Using HTTP](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-qmux-01)
Lucas Pardue and Eric Kinnear presented updates to `draft-ietf-quic-qmux`. Wire-breaking changes were finalized in `-01` (two-layer encoding using QMux records), and `-02` focused on non-wire-breaking behavioral hardening.

*   **Implementation & Interop Status:** Broad implementation progress (HAProxy, proxygen, picoquic, MSQuic fork, quiche/curl, and quic-go). HTTP/3 over QMux and Media over QUIC (MoQ) over QMux are current drivers for interop testing.
*   **Substrate Support:** Marco Forte advocated for allowing QMux over any suitable substrate. Kazuho Oku noted that non-TCP substrates handle closing differently and suggested focusing on TCP/TLS first, leaving other substrates to separate specifications. Jonathan Lennox agreed, suggesting that QMux over Unix domain sockets could be specified independently.
*   **Insecure Substrates and Cryptography:** A participant suggested allowing QUIC `CRYPTO` frames directly in QMux to ease implementation by leveraging existing QUIC/TLS machinery. Eric Kinnear, Lucas Pardue, Alan Frindell, and Marco Forte opposed adding this complexity, preferring to keep the core QMux protocol minimal and handle transport-level security via an external TLS layer or shim.
*   **ALPN on Non-TLS Substrates:** For cases like Unix domain sockets, the authors discussed how to negotiate the application protocol. Christian Huitema and Lucas Pardue favored treating this as a "substrate-specific problem" to avoid protocol mismatch risks in the core QMux specification. Kazuho Oku commented in chat that HTTP upgrade tokens specify the application, whereas QMux behaves as a substrate.
*   **Silent Close:** To prevent battery drain on mobile devices, Gorry Fairhurst (via Eric Kinnear) highlighted the importance of silent close for idle connections rather than forcing active wake-ups. Discussion was deferred to GitHub.

## Extended Key Update: [Extended Key Update for QUIC](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-extended-key-update-00)
Yaroslav Rosomakho presented updates to `draft-ietf-quic-extended-key-update`. The underlying TLS Extended Key Update (EKU) dependency consolidated handshake messages into a single EKU message with three subtypes (key update request, key update response, and new key update—the latter not used in QUIC). Additionally, the initial handshake transcript is now mixed into subsequent key derivations for stronger security properties.

*   **Discussion:** Magnus Westerlund questioned whether this overrides the standard QUIC rule against using TLS `CRYPTO` frames post-handshake. Yaroslav Rosomakho clarified that EKU leverages `CRYPTO` frames similarly to how New Session Tickets are handled. Magnus Westerlund noted that long-lived connections (e.g., BGP over QUIC) heavily require this post-compromise security. Yaroslav Rosomakho requested volunteers for interop testing using the prototype Rustls/Quinn implementation.

## Receive Timestamps: [QUIC Extended Acknowledgement for Reporting Packet Receive Timestamps](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-receive-timestamps-00)
Joseph Beshay presented updates to `draft-ietf-quic-receive-ts`. Version `-03` included minor editorial updates to the `max_receive_timestamps` transport parameter and a new security considerations section.

*   **Plausibility Checks & Clock Drift:** Ian Swett noted that malicious or drifting peer clocks could severely disrupt bandwidth-estimation congestion control algorithms (such as BBR), potentially leading to a 2x misestimation. He recommended adding a "SHOULD" guideline for performing plausibility checks. Alessandro Ghedini supported including default heuristic guidance in the draft to simplify implementation. Jonathan Lennox noted that timestamp-based algorithms must be robust against odd clock behavior, as peer clocks naturally drift. Gorry Fairhurst called for sanity checking on complex or unusual network paths.

## qlog: [qlog: Structured Logging for Network Protocols](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-qlog-00)
Lucas Pardue presented updates to `draft-ietf-quic-qlog-main-schema`, `draft-ietf-quic-qlog-quic-events`, and `draft-ietf-quic-qlog-h3-events`. The JSON-SEQ serialization format was retained. Visual tool support has improved with Pat Meenan's "waterfall tools" integrating qvis-like sequence views and Chrome NetLog visualization.

*   **Inconsistency in `frames_processed`:** Lucas Pardue outlined three options for resolving inconsistent frame event types across QUIC and HTTP/3 layers: (1) remove the `frames_processed` event entirely, (2) add a similar event to HTTP/3, or (3) keep the status quo. Kazuho Oku and Christian Huitema favored removing the `frames_processed` event to keep the schema simple. The authors will proceed with this removal.

## Reverso for QUIC: [Reverso for QUIC](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-reverso-for-quic-00)
Florentin Rochet proposed a non-backward-compatible protocol modification (requiring a new QUIC version) that places the Stream ID and Offset in the protected short packet header, reverses the relative order of frames, and mandates the stream frame to be first in the packet if any. This allows out-of-place decryption directly into contiguous application memory buffers, achieving zero-copy data delivery.

*   **Discussion:** Kazuho Oku liked the layout advantages (e.g., avoiding variable-length integer calculations before knowing where payload data begins) but questioned the appetite for a new QUIC version. Brian Trammell confirmed this would constitute an incompatible "QUIC v3". Lars Eggert and Christian Huitema questioned whether in-memory copy is indeed the primary bottleneck in real-world deployments compared to protocol complexity, and Christian queried if high-performance cases would use RDMA instead. Ian Swett encouraged the researchers to experiment further with radical wire-format changes if they are already willing to break compatibility.

## CTAPS: [TAPS - CTAPS and gaps](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-taps-ctaps-and-gaps-01)
An analysis of mapping QUIC to the IETF Transport Services (TAPS) architecture using "CTAPS", a C-based TAPS library.

*   **Discussion:** The presenter identified structural gaps: mapping a TAPS Connection Group to a QUIC Connection, and individual TAPS Connections to QUIC Streams. This model struggles with graceful closing semantics (where a stream is half-closed but still open for receiving), establishing unidirectional streams, and the granular aborting of individual streams (e.g., distinguishing between `RESET_STREAM` and `STOP_SENDING`). Brian Trammell noted that TAPS originally scoped out QUIC because the protocol was still in development. Eric Kinnear welcomed the implementation diversity. Lucas Pardue noted that design feedback should be directed to the TSVWG, as the TAPS Working Group has concluded.

## GCM-SST in QUIC: [GCM-SST in QUIC](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-gcm-sst-in-quic-00)
Magnus Westerlund proposed introducing AES-GCM Strong Secure Tags (SST) as a cipher suite option. It derives fresh authentication keys for each packet, allowing truncated 12-byte tags (saving 4 bytes per packet) while maintaining strong single-forgery limits. This is particularly advantageous for multipath and multicast scenarios where replayed forgery attempts might span multiple paths/receivers.

*   **Discussion:** Lars Eggert and Martin Duke discussed whether this work must be finalized in the TLS WG first. Magnus Westerlund confirmed that TLS registers the cipher suites, but QUIC defines the specific header protection mapping. David Schinazi emphasized that QUIC implementations must explicitly authorize and define parameters (such as minimum packet sizes and sampling offsets) for new TLS ciphers. He noted that the multicast use case would provide useful input for security experts evaluating the proposal.

## Mutable Idle Timeout?: [Mutable Idle Timeout?](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-mutable-idle-timeout-00)
Lucas Pardue explored dynamically updating the negotiated maximum idle timeout during a connection's lifetime (e.g., shrinking it after an HTTP/3 `GOAWAY` or shifting it during connection migration).

*   **Discussion:** Brian Trammell and "Speaker 27" (Marten Seemann(?)) noted potential utility in MASQUE, hole punching, or long-running connections migrated over changing NAT paths. Ian Swett expressed heavy skepticism regarding the added state-machine complexity, citing past issues with dynamic settings in HTTP/2. He emphasized that implementations should reliably close connections and inform peers of early timeouts to avoid tail latency. Valentin Goșu noted in chat that Firefox is currently seeing 0% of close reasons as idle timeouts, which Max Inden clarified was likely due to a local telemetry instrumentation bug.

## Telemetry on HTTPS RR and QUIC v2 adoption: [slides](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-telemetry-on-https-rr-and-quic-v2-adoption-00)
Max Inden presented telemetry from Firefox showing that the majority of HTTP/3 upgrades still rely on `Alt-Svc` headers (which require a prior HTTP/1.x or HTTP/2 connection) rather than HTTPS resource records (RR) via DNS. Additionally, QUIC v2 adoption remains extremely close to 0%. Max promoted his check tool (`savearoundtrip.com`) to help operators test their HTTPS RR and QUIC v2 support.

*   **Discussion:** David Schinazi pointed out that QUIC v2 does not fully prevent ossification on the critical upward path (client initials) because clients still offer v1 in their initial flights, meaning middleboxes can still ossify based on v1 initials.

## QUIC and Multicast: [slides](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-quic-and-multicast-00)
Max Franke and Louis proposed integrating single-source multicast into QUIC as an opportunistic extension. Unicast is used as the secure anchor to exchange shared keying material, while data is distributed over multicast. The presenters demonstrated two running implementations: an RTP-over-QUIC prototype from the hackathon and a Media over QUIC (MoQ) multicast extension running natively in a modified version of Firefox. Testing showed up to an 80% reduction in server egress traffic.

*   **Discussion:** Gorry Fairhurst raised concerns about multicast congestion control. Max Franke acknowledged the challenge but stated they have viable candidate solutions. François Michel suggested consolidating the two active individual drafts to align on keying, authentication, and the use of multipath. Security concerns regarding shared traffic keys among all receivers were discussed. To prevent packet injection by malicious receivers, the implementation uses asymmetric "integrity frames" (hashes sent via the secure unicast control channel) to verify packet authenticity. Etienne Dechamps and Magnus Westerlund discussed loss recovery, noting that clients can request unicast retransmissions for missed multicast packets. Ted Hardie (in chat) suggested this work might warrant a Birds of a Feather (BoF) session to gather feedback from security and operator communities.

## n0 NAT Traversal: [slides](https://datatracker.ietf.org/meeting/126/materials/slides-126-quic-n0-nat-traversal-00)
Floris Bruynooghe presented an implementation of peer-to-peer NAT hole punching over QUIC multipath, based on Marten Seemann's NAT traversal concepts. It coordinates peer discovery via a relay and uses "reach-out" frames containing candidate IP addresses alongside RFC 9000 `PATH_CHALLENGE` / `PATH_RESPONSE` frames.

*   **Discussion:** Floris Bruynooghe highlighted that managing connection IDs (CIDs) during aggressive path validation was highly challenging due to rapid CID consumption. They brought back off-path probing frames to separate path validation from connection migration. Marco Munizaga noted in chat that he and Marten Seemann recently updated [draft-munizaga-quic-alternative-server-address](https://datatracker.ietf.org/doc/draft-munizaga-quic-alternative-server-address/), which could serve as a useful building block for separate NAT traversal specifications.

## Decisions and Action Items
*   **`draft-ietf-quic-qmux`:**
    *   **Decision:** Keep the QMux core protocol simple. Reject the inclusion of QUIC `CRYPTO` frames inside QMux for non-TLS substrates; security on alternative substrates must be handled by external TLS layers or separate specifications.
    *   **Decision:** Frame negotiation (ALPN) on non-TLS substrates will not be solved within the core QMux draft (the "you problem" approach).
*   **qlog drafts** (`draft-ietf-quic-qlog-main-schema` / `draft-ietf-quic-qlog-quic-events` / `draft-ietf-quic-qlog-h3-events`):
    *   **Decision:** The `frames_processed` event will be removed to maintain schema simplicity.
    *   **Action:** qlog editors to remove `frames_processed` and prepare the documents for Working Group Last Call (WGLC).

## Next Steps
*   **`draft-ietf-quic-receive-ts`:** Joseph Beshay and Ian Swett to draft a Pull Request defining reasonable heuristics for identifying and rejecting implausible peer timestamps to protect congestion control algorithms.
*   **`draft-ietf-quic-extended-key-update`:** Authors to monitor progress of the EKU specifications in the TLS Working Group before triggering a QUIC WGLC.
*   **Multicast over QUIC:** Working group chairs and ADs to discuss the appropriate path forward (including a potential BoF) to address multicast congestion control and security models.

## Note on Minute Generation

These minutes are sourced from the AI-generated summary published at https://ietfminutes.org/minutes/ietf126/quic.html, which notes the content is AI generated and may contain mistakes. The chairs verified the contents and made some minor changes before publishing the draft minutes. The WG may have proposed additional changes.

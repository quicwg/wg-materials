# IETF 124: QUIC Working Group Session Minutes
**Date:** November 6, 2025
**Chairs:** Lucas Pardue, Matt Joras
**Note takers:** https://ietfminutes.org (AI generated and may contain mistakes)

## Summary
The QUIC Working Group met at IETF 125 to discuss the progress of active drafts, with a primary focus on the newly adopted QMux specification and proposals for RTT calibration and explicit network measurements. Key highlights included the advancement of the Multipath document through the IESG, implementation updates for qlog and receive timestamps, and technical refinements to QMux regarding its record layer and ALPN handling.

## Document Status Updates
*   **Multipath:** Lucas Pardue noted that the Multipath document has cleared IESG ballots and is effectively complete unless further issues arise.
*   **Shepherding:** `draft-ietf-quic-ack-frequency` and Reliable Reset are awaiting shepherd write-ups; progress is expected before the next meeting.
*   **draft-ietf-quic-extended-key-update:** Progress is currently gated by corresponding changes in the TLS working group.
*   **qlog:** `draft-ietf-quic-qlog-main-schema` and related drafts have seen implementation updates (e.g., Cloudflare's quiche). A virtual interim is planned.
*   **draft-ietf-quic-receive-ts:** Draft -02 is published with temporary code points. Authors encourage implementation and experimentation.

## QMux: [QMux](https://datatracker.ietf.org/meeting/125/materials/slides-125-quic-qmux-00)
Kazuho Oku led a discussion on several open issues and pull requests for `draft-ietf-quic-qmux`:

*   **Two-Layer Encoding:** A proposal to introduce a "QMux record" layer (a size-prefixed field containing frames) was discussed. This aligns QMux framing with QUIC v1 and facilitates porting to message-oriented transports like WebSockets. Alessandro Ghedini and Lucas Pardue supported this as a good compromise for implementation simplicity.
*   **Deadlock and Flow Control:** To prevent deadlocks on flow-controlled underlying transports (like TCP), the group agreed that the QMux stack must continue reading from the transport even if the application is blocked.
*   **ALPN and Protocol Identification:** Discussion centered on whether ALPN should identify the application protocol, the substrate (QMux), or a combination. The emerging preference is for the ALPN to designate the application protocol, which then specifies its use of QMux. Ben Schwartz and others noted that distinct ALPNs are needed for service discovery (e.g., HTTPS/SVCB records).
*   **Transport Parameters:** The group favored sending transport parameters via QMux frames rather than TLS extensions to maintain compatibility with TLS stacks that lack arbitrary extension APIs.
*   **Implicit Acknowledgments:** Since QMux often runs over reliable byte streams, the stack can assume data is acknowledged once written to the underlying transport.

### MoQT over QMux: [moqt-over-qmux](https://datatracker.ietf.org/meeting/125/materials/slides-125-quic-moqt-over-qmux-01)
Suhas Nandakumar presented challenges regarding advertising application protocols (like MoQT) over QMux. The discussion highlighted the need for a clear mapping between TLS ALPNs and the nested protocol layers.

### RTT Calibration: [Calibrating Minimum RTT Under Low ACK Frequency](https://datatracker.ietf.org/meeting/125/materials/slides-125-quic-calibrating-minimum-rtt-under-low-ack-frequency-00)
Tong Lee presented research showing that low ACK frequency (as proposed in `draft-ietf-quic-ack-frequency`) can bias minimum RTT estimations by 8-18%. The proposal involves reporting the timestamp of the specific packet that achieved the minimum one-way delay.
*   **Discussion:** David Schinazi suggested merging this effort with `draft-ietf-quic-receive-ts`. Christian Huitema offered to collaborate on incorporating these ideas into his related work.

### Explicit Measurement: [Application of Explicit Measurement Techniques for QUIC Troubleshooting](https://datatracker.ietf.org/meeting/125/materials/slides-125-quic-application-of-explicit-measurement-techniques-for-quic-troubleshooting-00)
Marcus Ihlar proposed a new explicit measurement layer for QUIC, using a dedicated packet type and version to allow on-path observers to measure loss and delay without exhausting short header bits.
*   **Discussion:** Ted Hardie and others argued that such a proposal requires a full Birds of a Feather (BoF) session before being considered for adoption, citing historical sensitivities regarding on-path telemetry (e.g., the spin bit and PLUS). Martin Duke expressed skepticism regarding endpoint implementer interest.

## Decisions and Action Items
*   **QMux:** The working group reached a tentative consensus to adopt the two-layer encoding (record layer) and the clarified flow control/deadlock prevention text in the next draft of `draft-ietf-quic-qmux`.
*   **ALPN:** The QMux draft will be updated to clarify that ALPN identifies the application protocol, with the underlying substrate requirement being implicit or handled by the application specification.
*   **Action Item:** Lucas Pardue and Matt Joras to complete shepherd write-ups for `draft-ietf-quic-ack-frequency` and Reliable Reset.

## Next Steps
*   A virtual interim session will be scheduled to focus specifically on `draft-ietf-quic-qmux` issues and `draft-ietf-quic-qlog-main-schema` progress.
*   Authors of the RTT calibration proposal are encouraged to coordinate with the authors of `draft-ietf-quic-receive-ts`.
*   Further discussion on explicit measurements will continue in the SCONE and
    IPPM contexts, with a potential BoF requirement noted.

## Note on Minute Generation

These minutes synthesize the **official video recording**, **human-generated notes**, **AI-generated summary**, and the **live chat log**.
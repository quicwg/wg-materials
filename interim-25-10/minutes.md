# QUIC Virtual Interim for Qlog

## Tuesday, October 14, 2025

Notetakers: Lucas Pardue, Robin Marx

## Chair Intro and administrivia (5 mins)
  * Scribes, Blue Sheets, Note Well
  * Purpose of the meeting
  * Agenda bashing

## Update on qvis

Robin updates group on updating qvis, ETA end of year for support for up-to-date qlog schemas

## Working through open issues collected at https://github.com/quicwg/qlog/issues

### define logging for Capsules - https://github.com/quicwg/qlog/issues/486

Should we include the capsule protocol in HTTP/3 schema?

The decision made early on it wasn't useful, but maybe time to reconsider to put it into HTTP/3 spec.

Marten: we can log datagrams now, but can't log anything about capsules atm
    need a framework of how we log the capsule (parsed/created)
    still before WGLC

Robin: no doubt it's useful, but do we want to include it here?
    will likely delay, because will open flood gates for other things to include as well

Kazuho: capsules are built on semantics, so it would be weird to define it in H3 document
    would prefer other document to capture capsuels (and other HTTP/3 semantics)
    We don't have HTTP semantics support

Lucas: would be ok to revisit past decision, work isn't that hard
    practically, it's easy enough to include HTTP semantics stuff in this document, doesn't worry me
        just think: why... maybe just spin up extension document that does this now and float it around in Montreal in a few weeks. Get feedback from people that are using capsule protocol

Mirja (chat): I think having a separate extension document for capsules would be fine. It's a quite specific thing.
    But I agree that having qlog for capsules would be really useful to debug masque stuff in future.

    It might be worth thinking briefly how qlog for capsules would look like to ensure we didn't miss any basics needed in the base qlog doc.

Marten: if there would be an HTTP semantics document, what else would that contain?
    Lucas: would be years worth of efforts again... HTTP is so huge. Would just do specific capsule draft.
        for capsules: want to log on-wire aspect, not necessarily behavioural

Marten: willing to propose new text inside current qlog by Montreal to discuss further then
    will then discuss with WG and capsule users. TODO Lucas: post this to WG ahead of time

Outcome: Marten to prepare a candidate proposal for how this could look and take it to montreal to engage folks (including in HTTP too) to help us make a decision.

### HTTP/3 frame RawInfo is confusing - https://github.com/quicwg/qlog/issues/484

Robin: gives context

Marten: currently have 3 ways of logging frame length
    1. FrameParsed / created
    2. FrameParsed.raw
    3. individual frames . raw

    propose: remove length and raw field from FrameCreated and FrameParsed, just keep it on the frames, because non-optional

Robin: does make sense for these specific events.
    TODO Marten: will propose text/PR to remove these
    TODO Robin: make new issue to re-eval this for other parts as well (e.g., Long Headers, StreamFrame)

Support for not duplicating information across the logging structures.

Outcome: make a PR to remove the field from HTTP3FrameParsed and HTTP3FrameCreated

### Why does HTTP3FrameCreated and HTTP3FrameParsed have a length field? - https://github.com/quicwg/qlog/issues/483

Support for not duplicating information across the logging structures. See also discussion above.

Outcome: make a PR to remove the field from HTTP3FrameParsed and HTTP3FrameCreated

### PacketHeader.flags should be replaced with individual values - https://github.com/quicwg/qlog/issues/471

Support for this PR.

Outcome: update PR to address some feedback and plan to merge

### How to log sending of path probe packets? - https://github.com/quicwg/qlog/issues/456

Marten: related to ECN logging. Currently only in packet_setn and datagram_sent events
        dont' do datagram_sent

Mirja: confusion around PathID usage
    in multipath, you can have multiple active tuples at the same time for one path
        also have a way to say: all these tuples belong to the same path, can only use one at a time

Kazuho: agree use of term path is confusing here; multipath draft uses "tuple" for this type of thing to tuple_id
    can maybe just rename to TupleID instead of PathID here

Mirja: maybe renaming to TupleID might indeed be better

Lucas: to be clear: for 456, we can just close without action. Need new issues to rename to TupleID/tuple_assigned
    New issue: https://github.com/quicwg/qlog/issues/487

Outcome: close with no action. Open new ticket to track track changing the name of path_id field.

### JSON-SEQ is painful - https://github.com/quicwg/qlog/issues/434

Lucas: I'm afraid this will be a blocking issue for the draft unfortunately
        Benefits and real pains

        personal opinion: just define newline-delimited as new format inside qlog to get around "non official format" issue
            (similar for new media types)

Robin: how difficult will people be if we don't use JSON-SEQ?
    Mirja: will definitely be questions; need a good reason on this. Difficult but not impossible
    Lucas: might have some JSON parsing experts that will give issues because we have to fully/formally define the new format and will get edge cases wrong; might get stuck in IETF Last Call

Robin: how about we just remove the steraming option from the main docs and keep it as extension?
    Lucas: hate that... really need a streaming solution and needs to be clear for interop
    Marten: also don't like the option to have both... need to just pick one format

Kazuho: I agree with Lucas's problem, but I think we will have that pain with JSON-SEQ too (so I do not mind dropping the streaming option entirely, as Robin suggested)
    Not sure if we would succeed in defining our own thing... would prohibit something explicitly defined in the JSON RFC. Don't have high hopes in getting non-JSON-SEQ through

Lucas: think we still need more thinking/input
    Robin: so in Montreal, we'll find out if people would object to us defining our own streaming JSON format in qlog?
        Lucas: correct

Not much has changed since last discussed. Another approach could be remove streaming format altogether. Proposal to present idea of defining our own newline streaming JSON in qlog itself at the next IETF meeting and gather more feedback.

Outcome: make a strawperson proposal for a qlog-specific newline json in qlog docs themselves to see how others in the IETF might feel

### Register application/qlog+json and application/qlog+json-seq media types - https://github.com/quicwg/qlog/issues/425

Related to above issue #434

### split up PacketHeader.flags - https://github.com/quicwg/qlog/pull/478

Marten: want to just leave out fixed/reserved bits. People will use extension/new events if needed for other things
Robin: agreed, but add 1 sentence of prose explaining we've left them out for that reason

### Discuss extensibility of extension points through type or group sockets - https://github.com/quicwg/qlog/issues/416

Outcome: Robin to prepare some text before Montreal

### Give concrete guidance on how to extend qlog - https://github.com/quicwg/qlog/issues/405

Outcome: Robin to prepare some text before Montreal

### Difference between negotiated vs actually accepted/enabled TPs - https://github.com/quicwg/qlog/issues/398

Kazuho: problem with this approach: assumes endpoint decides when to use something at the handshake,
        not always true
        Don't think we should be generalizing this as a concept

Mirja: At the point of time you receive the parameter you make a decision, which could be logged as an event
    Maybe just add some discusion that all this can happen, just not how to resolve it concretely

Kazuho: We just record TPs received, then when something happens at a later moment of the connection, lookup TPs and decide what to do
    Kazuho: no need to do this now

Robin: propose to close with no changes, but add some prose that indicates that this might happen and that people should define their own events to disambiguate if needed

Kazuho: +1 to no change, but point out that others can add events

Outcome: no design changes needed. An editorial PR may follow up to better describe some of the considerations

### Improve quic:stream_state_updated - https://github.com/quicwg/qlog/issues/374

Marten: can we use Owner as we do at other places?
        maybe Owner isn't the best term for this... maybej ust rename this to Initiator everywhere?

Marten: maybe just use this as a trigger?
    trigger indicates who initiated a state change (only useful for reset events)

    Kazuho: ok with trigger

Lucas: no strong opinion. Let's just close open PR; open 2 new PRs
    TODO Robin: open PR to add the trigger (and make stream_side non-optional)
    TODO Robin: open PR to rename owner to Initiator everywhere else

Outcome: Robin to prepare an alternative PR based on input during the meeting

### change STREAM and DATAGRAM frame definition to allow logging of frame payload - https://github.com/quicwg/qlog/issues/342

Lucas: extra payload field would be more work and not used a lot
        Marten: I indeed would not log this

Lucas: close with no action? nobody is actually complaining about this

Robin: you can also just read the payload by skipping the header bytes (length - payload_length is header length)
    Marten: that works

Outcome: proposed close with no action

### Is the loss_timer_updated event sufficient? - https://github.com/quicwg/qlog/issues/319

Marten: can argue there are not multiple timers. There's only the timer that fires first out of all the possible timers, and you just log the one that fires first (log when timer will next fire)
        Mirja: agreed, as long as we can log

Robin: maybe make timer_type extensible though, for other CCs
   ... bit of discussion of whether we need an idle timer etc. here as well
    Lucas: idle timer would change with every packet, so would be very chatty
        though maybe if we just make this a generic "timer_updated" and just make timer_type

    TODO Robin: make PR to update from loss_timer_updated to timer_updated, move timer_updated to QUIC, make timer_type extensible ENUM

Discussion on whether we have different timers or not
    Lucas: nginx definitely has different timer IDs that they set/update
        maybe add a timerID field
        Robin: I like that, then also conceptually able to have multiple timers of same type

Mirja: make makes sense to distinguish timers that are for the whole connection or per-path (or per-stream)

Marten: QUIC recovery only has one recovery timer, but several other types of timers
    e.g., abandoning path validation, handshake timeout, ...

    Mirja: at least having 1 generic way to log all timers would be useful. Though maybe would be intresting to split out recovery timers from general timers for clarity
        if it's workable with 1 event, then let's do that

    Kazuho: agree capability to log when each timer expires is useful

        Kazuho: what marten is saying, if there's one timer, then loss timer will probably always fire before idle timeout, so setting the idle timer would never be set in loss_timer_updated
            Kazuho: however, being able to know when each timer is expected to fire would also be useful
            Robin: agree, that was the original proposal

Outcome: make the timer more generic, PR to come

### Allow the logging of Session Ticket contents and stored transport params/SETTINGS - https://github.com/quicwg/qlog/issues/121

Marten: We have ways to log Token and StatelessResetToken. We could replicate that for the SessionTicket.

Mirja: logging session ticket is useful, not sure where to put it

Lucas: maybe useful to separate out

Kazuho: if we go down to the TLS level, things get messy (encrypted, obfuscated, etc.)
    maybe only log QUIC-accessible part of the session ticket blob

    Robin & Marten: love that suggestion; let's do it like that

    Mirja: things that are only in RFC9001 should not be in here ,but things that might be in 9000 might make sense

Outcome: Marten to propose a PR

### Add more TLS-specifics - https://github.com/quicwg/qlog/issues/59

### 0-RTT is a bit ambiguous in -01 - https://github.com/quicwg/qlog/issues/27

Lucas: implementation experience: haven't found much lacking in qlog here
        if we have bugs, it's deep inside TLS anyway, and we need TLS tooling for that anyway

Kazuho: really only from the client viewpoint. For a Server, you either just accept 0-RTT or not
    from client side, could make many more decisions
    might be a good idea to ask client-side developers if they have an opinion

Marten: we might not be able to log if server rejects 0-RTT in TLS handshake at the client
    at server-side it's easy: just drop packet
    at client-side we do want to be able to log that, since that influences how we re-use the stream etc.

Mirja: new issue: might want to log packet number space for more than just ACKs

Outcome 1: logging 0-rtt accepting / rejection seems useful; @marten-seemann will prepare a PR for that. In addition, ask client implementers if there are any other gaps.

Outcome 2: Mirja will review with the context of multipath and packet spaces and maybe open issue(s)


### PR: remove PacketHeader.length - https://github.com/quicwg/qlog/pull/477

Mirja: I'm a bit on the fence. Seems like rawinfo is more like debugging/helper, not for general use
        in that sense, having length right there makes sense
        However: having multiple ways for the same thing isn't good

        Potentially just clarify that rawinfo is additional if you need it, not the default way

Lucas: don't think I've ever logged length in the PacketHeader...
    I just use rawInfo instead

Robin: also look at #480
    Mirja: consistency is more important than ergononmics, even if wrapping in rawinfo is a bit clunky

TODO Robin: make new, big PR that makes this consistent (remove length fields, add prose indicating raw.length should be used)
    Close other PRs and issues for this
    TODO Robin: create new issue to track this
    Mirja: also add text that makes it very clear that logging lengths is useful (even if rawinfo is optional)

### PR: improve description of StreamFrame.offset and length - https://github.com/quicwg/qlog/pull/480

Related to PR above.

## IETF-121 QUIC WG Agenda

## Wednesday, November 6, 2024

09:30-11:30 Wednesday, Session I

### Administrivia
5 min total

Implementation status of ACK frequency and reliable reset discussed.

Lars: Mozilla has implemented an old draft version of ack frequency.

Mirja: Ericsson has two implementations of ack-freq.

Magnus: Accidentally detected ack-frequency interop during MP-QUIC

Mike B: Few implementations is a sign that it's not urgent?

Christian H: Pico-QUIC has an implementation. Was assuming it's in RFC editors queue. If not, there is an issue with compatibility between ack-frequency and MP-QUIC. An MP-Ack frequency is required.

David S: Web transport has a need for Reliable Rests. People at Google have been working on implementation. Status: close..

Mirja K: If we want to do something with ack-freq and MP-QUIC it should be done in MP-QUIC.

Alan F (MOQ chair): MoQ has a dependency on reliable resets as well. Implementation at Meta.

Kazuho: Fastly has implementation of both.

Martin D: How many interoperable implementations do we need?

Zahed: It's not the number that matters, it's the quality. Let's target next hackathon for interop test event. Keep in mind that QUIC WG has a high bar on interoperability.

David S: Ack freq is different since it's a perfomance feature. Exchanging frames is one thing, but deploying at scale and learning might be required for understanding that the spec is complete.

Mirja K. Exchanging frames is easy. The rest can't be interoped. We can't wait for learning about other issues.

Kazuho: Agree with Mirja. Waiting for browsers to implement.

**Matt (chair): Chairs will follow up on interop test event for reliable resets.**

### WG Items

#### 40 min - Open issues, updates to multipath QUIC. slides

Issue 455 - resolved in PR
Pr 462 fixes encoding error.
Issue 461 - resolved in PR

No discussion on above.

Issue 459:

Eric K: Can we change the max path ID instead?

Mirja K: No, it's going in the wrong direction. what we are talking about is how to tell a peer that we don't have CIDs.

Eric: Make this condition impossible by always giving CIDs with paths.

Mirja: this is what the draft is trying to do, but can not be guaranteed.

Christian: This is asynchronous, it's not possible to make this condition impossible.

No resolution agreed. The solution for the next issue might work?

Issue 414:

Magnus W:

Lucas (as error code enthusiast): If you expect a reaction for a peer to do something, error codes are not a good choice. The space is too large. For a reaction to happen use a different field, the field can be enhanced by an error code though.

Mirja: Two cases, one is an error and one can be acted upon.

Lucas will comment on PR.

Christian: No new error code, rather new frame. New frame is more expressive.

**Resolution: Create a new PR and have discsussion there.**

Issue 457:

Christian Huitema: There is nothing in RFC 9000 that prevents you from the same frame many times on several paths. We have several implementations already doing that, it's not impossible.

Pico QUIC does this on the first PTO.

A note could be there with some consideration.

Eric K is in agreement with Christian, but could be slightly more aggressive.

Mirja: it's allowed, but how aggressive should we recommend.

Eric: Marginally more aggressive.

Magnus: Agrees but points out that a bullet on the slide is wrong. You need to get some data across to declare data being lost.

Matt (as an individual): We don't know what's better guidance here. Leave this up to implementations.

Jana I: Being aggressive is in relation to what you have. If your congestion window allows, there is nothing that prevents you to send your data.

**(resolution seems to be to write some guidance, but how detailed/aggressive seems to need discussion)**

Issue 458:

Christian: RFC has the mechanism for path migration by testing several CIDs in parallel and take the one we like. The RFC 9000 migration is clunky. With MP we create a new path and put it in backup state..
Using path migration in the old way adds complexity that hurts. NAT rebinding can be supported, it's way simpler.
PROPOSAL: support rebinding but do not support RFC9000 migration.

Lorenzo C: Make before break sounds nice, but cellular is very expensive for the the battery.
Firewall timeouts are very small. Even with a backup you need to keep it alive for really long. There are conditions where you might need to keep your cellular up for 25% of the time.

Christian: Agrees that you need to take care with keeping paths up. But this is an implementation consideration.

Lorenzo: You don't have this problem with connection migration without having to pre-warm a path.

Eric K: We don't need to pre-warm minutes before, rather seconds, we get indications that wifi gets bad. The question is how do we spell this out, do we allow two ways or just use multipath. It's probably ok to allow only one way.

Lorenzo: Is not commenting on specific approach, more about the properties of pre-warming etc.

Mike B: Is there something fundamentally different between path switching in new or old way?

Christian: An explicit path is cleaner since you have a new stateful congestion control.

Mike: Migration already requires you to reset that. Could a client game that by not changing the path ID?

Jana: There will be overlap between migration and multipath, we knew that from the start.

Mirja: We need migration for rebinding. For the other case we have two mechanisms.

**(no clear resolution to discussion)**

Author asks for WGLC.

Show of hands: Have you read a recent version of the multipath draft?
Yes: 14
No: 30
No opinion: 2

Lars E: Wrt to WGLC. Struggling with this document, covers a lot of ground. Points out that there is no parts that deal with congestion control and scheduling etc. Claims that if you implement the draft you can do MP are over stated. Therefore going for a standards track document that only talks about how to explicitly set up paths.

Some parts are ready and can go forward, others I have reservations about.

Mirja: I think this is what the draft is doing.

Lars: The result we have now is that some pieces are more baked than others. Let's find something to move forward with. If it's a take it or leave it thing we shouldn't move forward.

Mirja: I think this is what we do already.

Lars: This might be a scoping issue. You can't just read this draft and get generic multipath. Establishing and maintaining multiple paths is what I could implement. The draft should explicitly say that you get parts of multipath.

Mirja: Agrees, but there is likely editorial passes to be made.

Lucas chair: I would like to see editorial restructuring and reviews from WG participants.

Brian: There seems to be confusion around about what we specify and what you need to bring on your own. We did that with QUIC as well.

**The chairs will have a chat about this and coordinate with editors teams. At least one draft revision will be needed before WGLC.**


**Timelines? Could an interim help progress these last issues faster?**

**An interim can be considered.**

#### 20 min - Open issues, updates to qlog.

Issue 319:
Seeks review on this topic.
No comments.

Issues 132 and 444:
Lucas presents an idea and seeks feedback.
No comments.

Bikeshed discussion on serialization formats.
JSON-SEQ is the current format, other options are not standardized and WG might need to get involved in ongoing discussions.

Describes some issues with JSON-SEQ, including the lack of support in several out-of-the box text tools.

Proposed resolutions:
1. Do nothing - keep JSON-SEQ
1. Switch to something else.
1. Add another one.
1. Do not normatively recommend any serialization.

Martin Seeman: JSON-SEQ is painful for several reasons. You can't type the record separator.. A common UC for QLOG is to look at a trace and see some issue. You can type a filter expression in JQ, but it's painful. Grep is more convenient. This is more painful with JSON-SEQ. Grep requires a transform step..

Martin Thomson: Does not have as strong opinion on the outcome. But feel strongly that: pick one and only one.

Lucas: Should there only be one? Yes, an argument against option 3.

Eric: We chose a human readable format initially, and now we don't have tooling support.

Lucas: You can adapt your output based on your intended use. You don't need to use the full suite of capabilities.

Matt: The alternative solutions are not RFCs. This was a significant consideration when we picked JSON-SEQ. This will come up in any of the options.

Brian: Agrees with Martin. IETF is used to the serialization format and user experience being the same thing. This is not the case. Tooling can be built.

Robin M: Acks Matt's point that there was fear that picking non-RFC formats were regarded as a big issue. Would like to hear more about whether this is the case.

**Resolution: there's a goal of WGLC by end of year. Issues need to be resolved..**

### Other (aka "As Time Permits")

#### 15 min - Address Discovery (Marten Seemann)

Extension used for signalling observed addresses for paths.

Lorenzo C: What if the Masque server does not have a public IP. Would you use STUN with this?

Marten: You could chain proxies.. you would need to deal with this. Use of multiple nodes..

Jaroslav??: If you have a client is on path that uses per packet load-balancing. Here you would receive this frame per packet. Rate limiting?

Marten: You describe a NAT rebinding that happens very often (looks like that to the server). RFC 9000 sees this as an attack. Do the same thing as for path validation.

Antoine: Is there a way for a proxy involved in address coordination to not be involved in relaying traffic.

Marten: this would need to be worked out.

David S: What's your goal, adoption?

Marten: Adoption.

David S: We already have a solution that we didn't adopt because we don't have a need for it. If we don't have a Use Case let's not adopt.

**Show of hands: Is this something the QUIC WG should work on? (clarification NOW-ish)**
Yes: 19
No: 7
No opinion: 19

#### 10 min - Flexicast QUIC (Louis Navarre)

Not seeking adoption, but does seek feedback and collaboration.

Lucas as an enthusiast: This draft will get more discussion in MBONE, if you're interesting in multicast stuff go there.

Francoise: Looks like clever research work. Would like to see you present new stuff. Will ask more questions later.

#### Final comments
Come check out deepspace for QUIC topics.

AD is happy with the session :D
# Member Services Voice Agent — Product Brief (draft)

*Status: early draft. Putting down what we know so far so design can start.*

## Problem

Our payer call center reps spend too much time on routine member calls —
status checks, eligibility questions, simple claim lookups — and then have to
manually write up the call afterward. Wrap-up takes forever and notes are
inconsistent. We want an AI voice agent that can handle the easy calls and do
the write-up automatically.

## Objective

Stand up a voice agent that answers common member questions and, at the end of
the call, creates the case and writes the summary on its own. If it can't
handle something, it should pass the caller to a human. The end result should
look the same whether a human or the agent handled the call.

## What it should do

- Take inbound member calls
- Figure out who's calling
- Answer common questions (eligibility, benefits, claim status)
- Create a case for the issue
- Write a summary at the end and save it
- Hand off to a human when needed
- Maybe send a follow-up email

## Success looks like

- Reps spend less time on wrap-up
- Members get answers faster
- Fewer calls need a human

## Notes

This is a payer/health use case so there's member data involved — we'll need to
be careful about that. Timeline is this release if possible. Will fill in more
detail after design review.

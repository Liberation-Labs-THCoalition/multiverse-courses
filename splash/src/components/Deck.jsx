'use client';

import { useState, useEffect, useMemo, useRef, useCallback } from 'react';
import Stack from './Components/Stack';
import deckData from '../deck/cards.json';
import './Deck.css';

// The content is final: every word comes from cards.json, rendered here and never
// reworded. This component only adds the interaction around it.
const CARDS = deckData.cards;
const TOTAL = CARDS.length;

// The player's picks are remembered in localStorage only, wrapped in try/catch so a
// disabled / unavailable storage never breaks the deck. Nothing leaves the browser.
const STORE_KEY = 'vibe-research.deck.picks.v1';

function loadPicks() {
  try {
    const raw = window.localStorage.getItem(STORE_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return parsed && typeof parsed === 'object' ? parsed : {};
   } catch {
    return {};
   }
}

function savePicks(picks) {
  try {
    window.localStorage.setItem(STORE_KEY, JSON.stringify(picks));
   } catch {
    /* storage disabled or unavailable: the deck still works, just without memory */
   }
}

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );
}

// A fresh card has been seen, not inspected, not committed, not revealed.
function freshState() {
  return { inspected: false, commit: null, revealed: false };
}

// The next card, shown fanned behind the active one via React Bits' Stack. Read-only:
// it is the "rest of the deck", not a control.
function PreviewCard({ card }) {
  return (
    <div className="peek">
      <div className="peek-title">{card.title}</div>
      <div className="peek-mystery">{card.mystery}</div>
    </div>
  );
}

// One card of the deck: mystery -> inspect the evidence -> commit a prediction -> reveal.
// The reveal flips the card over (plain CSS 3D transform) to show the reveal, its
// sources, (for the invented study) the fiction notice, and the "you predicted before
// you looked" line. There is no correct/wrong mark and no score anywhere.
function MysteryCard({ card, state, onInspect, onCommit, onReveal }) {
  const reduced = prefersReducedMotion();

  // A card that is already revealed is shown with its evidence open, so the flip has a
  // full-height front face to rotate away from.
  const showEvidence = state.inspected || state.revealed;

  return (
    <div
      className={`deck-card${state.revealed ? ' is-revealed' : ''}`}
      data-card-id={card.id}
      data-fictional={card.fictional ? 'true' : 'false'}
      aria-label={`Card: ${card.title}`}
    >
      <div className="deck-card__inner">
        {/* Front: the mystery, and (once inspected) the evidence and the commit. */}
        <div className="deck-face deck-face--front" aria-hidden={state.revealed || undefined}>
          <h3 className="deck-title">{card.title}</h3>
          <p className="deck-mystery">{card.mystery}</p>

          {showEvidence ? (
             <>
              <p className="deck-inspect">{card.inspect}</p>

              <div
                className="deck-commit"
                role="group"
                aria-label={`Your prediction on ${card.title}`}
              >
               {card.fictional ? (
                 // The invented study: the single commit is the fix, not a right/wrong guess.
                <button
                 type="button"
                 className="deck-btn"
                 data-committed={state.commit === 'axis' ? 'true' : undefined}
                 onClick={() => onCommit('axis')}
                >
                 Fix the axis (metres → centimetres)
                </button>
              ) : (
                 <>
                  <button
                   type="button"
                   className="deck-btn"
                   data-committed={state.commit === 'holds' ? 'true' : undefined}
                   onClick={() => onCommit('holds')}
                  >
                   It holds up
                  </button>
                  <button
                   type="button"
                   className="deck-btn"
                   data-committed={state.commit === 'apart' ? 'true' : undefined}
                   onClick={() => onCommit('apart')}
                  >
                   It falls apart
                  </button>
                 </>
              )}
             </div>

             <div className="deck-controls">
              {/* The reveal stays disabled until a prediction is committed. */}
              <button
               type="button"
               className="deck-btn deck-btn--reveal"
               disabled={!state.commit || state.revealed}
               onClick={onReveal}
              >
               Turn it over
              </button>
             </div>
            </>
          ) : (
             <div className="deck-controls">
              <button type="button" className="deck-btn" onClick={onInspect}>
                Inspect
              </button>
             </div>
          )}
        </div>

        {/* Back: the reveal, its sources, the fiction notice (invented study only), and
            the "you predicted before you looked" line. */}
        <div
          className="deck-face deck-face--back"
          aria-hidden={!state.revealed || undefined}
        >
          <p className="deck-reveal">{card.reveal}</p>

          {card.fictional && (
            <p className="deck-fict-notice" role="note">
              {card.fiction_notice}
            </p>
          )}

          {card.sources && card.sources.length > 0 && (
             <div>
              <div className="deck-sources-label">Sources</div>
              <ul className="deck-sources">
               {card.sources.map((source, i) =>
                 source.url ? (
                   <li key={i}>
                     <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                     >
                      {source.label}
                     </a>
                   </li>
                ) : (
                   // No URL: show the label, never invent a link.
                   <li key={i} className="deck-source-nolink">
                     {source.label}
                   </li>
                )
              )}
              </ul>
            </div>
          )}

          <p className="deck-predicted-line">You predicted before you looked.</p>
        </div>
      </div>
    </div>
  );
}

// The closing panel, shown after card 6.
function ClosingPanel({ closing, onReplay }) {
  return (
    <div className="deck-closing">
      <h3>{closing.question}</h3>
      <p>{closing.body}</p>
      <button type="button" className="deck-replay" onClick={onReplay}>
        See the deck again
      </button>
    </div>
  );
}

export default function Deck() {
  // index 0..TOTAL-1 are the cards; index === TOTAL is the closing panel.
  const [index, setIndex] = useState(0);
  const [picks, setPicks] = useState(() => loadPicks());
  const [reducedMotion, setReducedMotion] = useState(false);
  const swipeRef = useRef(null);
  const swipeStart = useRef(null);
  const announce = useRef(null);

  useEffect(() => {
    setReducedMotion(prefersReducedMotion());
    const mq = window.matchMedia
       ? window.matchMedia('(prefers-reduced-motion: reduce)')
       : null;
    const onChange = () => setReducedMotion(prefersReducedMotion());
    if (mq && mq.addEventListener) mq.addEventListener('change', onChange);
    return () => mq && mq.removeEventListener && mq.removeEventListener('change', onChange);
   }, []);

  // Remember the picks, but only the ones that exist, so we never clobber a fresh
  // entry with a stale one.
  useEffect(() => {
    savePicks(picks);
   }, [picks]);

  const card = index < TOTAL ? CARDS[index] : null;

  const stateFor = id => picks[id] || freshState();

  const update = useCallback((id, patch) => {
    setPicks(prev => {
      const current = prev[id] || freshState();
      const next = { ...prev, [id]: { ...current, ...patch } };
      return next;
     });
   }, []);

  const goTo = useCallback(
    target => {
      setIndex(Math.max(0, Math.min(TOTAL, target)));
     },
    []
  );
  const next = useCallback(() => goTo(index + 1), [goTo, index]);
  const prev = useCallback(() => goTo(index - 1), [goTo, index]);

  // Arrow keys navigate when the deck (or anything in it) holds focus.
  const onKeyDown = useCallback(
    e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        next();
       } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        prev();
       }
     },
    [next, prev]
   );

  // Swipe / drag on touch (and mouse drag on the card): a horizontal flick turns to
  // the next or previous card. The gesture is instant under reduced motion.
  const onPointerDown = e => {
    swipeStart.current = { x: e.clientX, y: e.clientY, t: Date.now() };
   };
  const onPointerUp = e => {
    const start = swipeStart.current;
    swipeStart.current = null;
    if (!start) return;
    const dx = e.clientX - start.x;
    const dy = e.clientY - start.y;
    if (Math.abs(dx) < 40 || Math.abs(dx) <= Math.abs(dy)) return;
    if (dx < 0) next();
    else prev();
   };

  // The fanned "rest of the deck" behind the active card (React Bits Stack).
  // Memoised on index so Stack's internal effect doesn't loop on new array identity.
  const peek = useMemo(
    () =>
      index < TOTAL
        ? CARDS.slice(index + 1, index + 3).map(c => <PreviewCard key={c.id} card={c} />)
        : [],
    [index]
  );

  const state = card ? stateFor(card.id) : freshState();

  return (
    <section
     className="deck"
     id="deck"
     aria-label="The mystery deck"
     tabIndex={0}
     onKeyDown={onKeyDown}
    >
     <p className="deck-heading">The mystery deck</p>
     <p className="deck-intro">{deckData.intro}</p>

     <div
      className="deck-stage"
      onPointerDown={onPointerDown}
      onPointerUp={onPointerUp}
      ref={swipeRef}
     >
      {index < TOTAL ? (
        <>
         {peek.length > 0 && !reducedMotion && (
           <div className="deck-peek" aria-hidden="true">
             <Stack
              cards={peek}
              autoplay={false}
              sendToBackOnClick={false}
              sensitivity={99999}
             />
           </div>
         )}

         <MysteryCard
          card={card}
          state={state}
          onInspect={() => update(card.id, { inspected: true })}
          onCommit={commit => update(card.id, { commit })}
          onReveal={() => update(card.id, { revealed: true })}
         />
        </>
       ) : (
        <ClosingPanel closing={deckData.closing} onReplay={() => goTo(0)} />
       )}
     </div>

     {index < TOTAL && (
       <div className="deck-nav">
         <button type="button" className="deck-btn" onClick={prev} disabled={index === 0}>
          ← Prev
         </button>
         <span className="deck-count" aria-live="polite">
          card {index + 1} of {TOTAL}
         </span>
         <button type="button" className="deck-btn" onClick={next}>
          Next →
         </button>
       </div>
     )}

     {/* The reveal is announced to screen readers when it appears. */}
     <div className="sr-only" role="status" aria-live="polite" ref={announce}>
      {card && state.revealed ? `${card.title}. ${card.reveal}` : ''}
     </div>
    </section>
  );
}

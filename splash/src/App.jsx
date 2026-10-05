import { useState, useEffect, useCallback, useRef } from 'react'
import DotGrid from './components/backgrounds/DotGrid'
import DecryptedText from './components/textAnimations/DecryptedText'
import CountUp from './components/textAnimations/CountUp'
import TrueFocus from './components/textAnimations/TrueFocus'
import StarBorder from './components/animations/StarBorder'
import Deck from './components/Deck'
import './App.css'

// The teaser counts up to this in the big number, holds, then glitches to GLITCH_TO.
// 2026-09-29: theory of mind (93 -> 20). The first version used a case reserved for a class session;
// the page every student sees first must never give away a class answer (see docs/site-spec.md).
const COUNT_TO = 93
const GLITCH_TO = '20%'
const HOLD_MS = 1000

export default function App() {
  const [showGlitch, setShowGlitch] = useState(false)
  const [countFinished, setCountFinished] = useState(false)
  const [glitchNumber, setGlitchNumber] = useState(`${COUNT_TO}%`)
  const [hoveredOutlier, setHoveredOutlier] = useState(false)
  const countRef = useRef(null)

  // Stable identity: otherwise any App re-render (e.g. hovering the outlier) restarts the count.
  const handleCountFinish = useCallback(() => {
    setCountFinished(true)
    setTimeout(() => {
      setShowGlitch(true)
      setGlitchNumber(GLITCH_TO)
    }, HOLD_MS)
  }, [])

  // CountUp's onEnd fires on a timer (delay + duration) while its spring is still easing in:
  // the number reads short of COUNT_TO at that moment. The 1 s hold has to start when the big
  // number actually READS COUNT_TO, so watch what CountUp renders instead. Compare NUMERICALLY:
  // CountUp prints whole numbers without a decimal ("93"), so an exact-text match on "93.0" would
  // never fire, and the teaser would sit on 93 forever without an error.
  useEffect(() => {
    const el = countRef.current
    if (!el) return
    let fired = false
    const observer = new MutationObserver(() => {
      const shown = parseFloat(el.textContent.replace(/[^0-9.]/g, ''))
      if (!fired && shown >= COUNT_TO) {
        fired = true
        observer.disconnect()
        handleCountFinish()
      }
    })
    observer.observe(el, { childList: true, characterData: true, subtree: true })
    return () => observer.disconnect()
  }, [handleCountFinish])

  const sessionTitles = [
    'The Question',
    'Designing to Fail',
    'Reading What Came Back',
    'The Gate and the Room'
  ]

    // The "See how: play the deck" button scrolls to the deck section below.
  const scrollToDeck = () => {
    const el = document.getElementById('deck')
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }

  return (
    <div className="app">
      {/* Background: subtle, reads as a scatter plot rather than a light show */}
      <div className="background-layer">
        <DotGrid
          dotSize={4}
          gap={28}
          baseColor="#1e2446"
          activeColor="#46508c"
          proximity={120}
          shockRadius={180}
          shockStrength={3}
        />
      </div>

      {/* Outlier easter egg - absolutely positioned, doesn't move with cursor */}
      <div
        className={`outlier-dot ${hoveredOutlier ? 'hovered' : ''}`}
        data-easter-egg="outlier"
        aria-label="the outlier"
        onMouseEnter={() => setHoveredOutlier(true)}
        onMouseLeave={() => setHoveredOutlier(false)}
      >
        {hoveredOutlier && (
          <div className="outlier-tooltip">
            You found the outlier. Most pipelines drop this one.
          </div>
        )}
      </div>

      {/* Main content */}
      <div className="container">
        {/* Hero section */}
        <section className="hero">
          <h1 className="hero-title">
            {/* DecryptedText hides its own text from screen readers, so say it once here */}
            <span className="sr-only">Vibe Research</span>
            <DecryptedText
              text="Vibe Research"
              speed={50}
              animateOn="view"
              sequential
              revealDirection="start"
              encryptedClassName="encrypted"
            />
          </h1>
          {/* TODO(Thomas): real tagline */}
          <p className="tagline">A research cycle with your agent</p>
        </section>

        {/* Teaser section */}
        <section className="teaser">
          <div className="teaser-number">
            {countFinished ? (
              <div className={`number ${showGlitch ? 'glitch' : ''}`}>
                {glitchNumber}
              </div>
            ) : (
              <div className="number">
                <span ref={countRef}>
                  <CountUp from={0} to={COUNT_TO} duration={1} />
                </span>
                %
              </div>
            )}
          </div>
          {showGlitch && (
            <div className="teaser-text fade-in">
              <p className="teaser-description">
                In 2023, a language model was reported to solve 93% of classic theory-of-mind tasks, as if theory of mind had spontaneously emerged. Tested properly, with matched controls, the same model solved 20%.
              </p>
              <p className="teaser-citation">
                Kosinski (2023; PNAS 2024) · Ullman (2023), "Large Language Models Fail on Trivial Alterations to Theory-of-Mind Tasks"
              </p>
            </div>
          )}
            {showGlitch && (
              <div className="teaser-deck-cta fade-in">
                <button type="button" className="teaser-deck-btn" onClick={scrollToDeck}>
                  See how: play the deck
                </button>
              </div>
            )}
        </section>

          {/* Mystery deck: the teaser, made playable. It is always on the page for
              visitors who scroll; the "See how: play the deck" button jumps here. */}
          <Deck />

        {/* Sessions section */}
        <section className="sessions">
          <div className="sessions-label">Sessions</div>
          <div className="sessions-strip">
            <TrueFocus
              sentence={sessionTitles.join('|')}
              separator="|"
              blurAmount={3}
              borderColor="#8b93c9"
              glowColor="rgba(139, 147, 201, 0.5)"
              animationDuration={0.5}
              pauseBetweenAnimations={2}
            />
          </div>
        </section>

        {/* CTA section */}
        <section className="cta">
          <StarBorder
            as="a"
            href="course/"
            className="cta-button"
            color="#8b93c9"
            speed="6s"
            backgroundColor="#0a0e27"
            textColor="#e0e0e0"
            borderColor="#2a3160"
          >
            Read the course
          </StarBorder>
        </section>

        {/* Footer */}
        <footer className="footer">
          Developed in public. Gaps are part of the process.
        </footer>
      </div>
    </div>
  )
}

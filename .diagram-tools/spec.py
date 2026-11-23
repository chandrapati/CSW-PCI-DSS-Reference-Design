"""Framing text for this framework's diagram.

Step content comes from the reference design; only the framing below is
authored.
"""

SIX_STEP = {'kicker': 'PCI DSS v4.0',
 'title': 'The 6-Step CSW Build',
 'title_tail': '&mdash; PCI DSS',
 'sub': 'The end-to-end path from &ldquo;CSW installed&rdquo; to QSA-ready evidence. '
        'Steps 1&ndash;4 stand it up; 5&ndash;6 keep it compliant.',
 'names': {1: 'Instrument',
           2: 'Label &amp; scope',
           3: 'Baseline with ADM',
           4: 'Author policy',
           5: 'Simulate, then enforce',
           6: 'Operate &amp; export'},
 'caution_label': 'Cadence &rsaquo;',
 'caution': 'Refresh <b>ADM every 90 days</b> and re-run scope reconciliation. The '
            'loop back from step 6 to step 3 is what keeps the CDE boundary accurate '
            'between assessments &mdash; Requirement 12.5.2 is a scope-accuracy '
            'requirement.',
 'takeaway': 'Every step names its own exit criteria and the artifact it produces, '
             'so the quarterly binder assembles itself. <b>A logged denied '
             'connection is the proof the control operates</b>, not just that it '
             'exists.',
 'rail': ['Default-deny on the CDE, with every permitted path explicit',
          'Simulation turns would-be outages into change tickets',
          'A repeatable binder a QSA can consume without a walkthrough']}

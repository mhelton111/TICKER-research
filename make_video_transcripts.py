from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent / "videos"
OUT.mkdir(exist_ok=True)

def make(filename,title,goal,sections):
    def p(text, style='Body', center=False):
        align='<w:jc w:val="center"/>' if center else ''
        return f'<w:p><w:pPr><w:pStyle w:val="{style}"/>{align}</w:pPr><w:r><w:t>{escape(text)}</w:t></w:r></w:p>'
    body=[p(title,'Title',True),p('Project 2 speaking script and transcript','Subtitle',True),p('Purpose: '+goal),p('Use this as a guide while recording. Speak naturally, pause when changing screens, and only say statements you can verify in the app or saved files.')]
    for heading,lines in sections:
        body.append(p(heading,'Heading1'))
        body.extend(p(line) for line in lines)
    body.append(p('Educational analysis only. This is not investment advice.','Heading2'))
    document='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'''+''.join(body)+'''<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1008" w:right="1224" w:bottom="1008" w:left="1224"/></w:sectPr></w:body></w:document>'''
    styles='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Aptos" w:hAnsi="Aptos"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Body"><w:name w:val="Body"/><w:pPr><w:spacing w:after="140" w:line="300" w:lineRule="auto"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:sz w:val="40"/></w:rPr><w:pPr><w:spacing w:after="100"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:rPr><w:sz w:val="22"/></w:rPr><w:pPr><w:spacing w:after="220"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="Heading 1"/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr><w:pPr><w:spacing w:before="220" w:after="100"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="Heading 2"/><w:rPr><w:b/><w:sz w:val="24"/></w:rPr><w:pPr><w:spacing w:before="180"/></w:pPr></w:style></w:styles>'''
    types='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'''
    rels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'''
    docrels='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''
    with ZipFile(OUT/filename,'w',ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',types); z.writestr('_rels/.rels',rels); z.writestr('word/document.xml',document); z.writestr('word/styles.xml',styles); z.writestr('word/_rels/document.xml.rels',docrels)

common_open=[
"Hello. This is my Project 2, the Meridian Reserve Decision Desk. It is an educational portfolio process, not investment advice.",
"The decision I am presenting is pilot, not adopt. I will explain the mandate, the calculations, the stress test, and the condition that would change my decision."
]
make('Video_1_Research_Evolution_Transcript.docx','Video 1 Research Evolution', 'Explain how the process became more decision-ready and show one AI-assisted output that was checked.', [
('Opening',common_open),
('Start with the mandate',[
"The mandate comes from the earlier portfolio labs. The objective is a 6.5 percent estimated annual return. The portfolio must hold at least 3 percent in BIL or IEF reserve assets. It is long-only and uses 5 percent weight increments.",
"I kept the 60 percent VTI and 40 percent LQD portfolio as a transparent reference baseline. I also show equal weight. Keeping both baselines visible makes it harder to hide a bad tradeoff behind one selected answer."
]),
('What changed in my thinking',[
"At first, a portfolio that had the highest estimated return could look attractive. The baseline comparison changed that. The 60/40 reference has a 7.15 percent estimated return, but it has zero percent in BIL or IEF. It fails the reserve rule.",
"The constrained portfolio meets both checkable rules. It is 65 percent BIL, 30 percent VTI, and 5 percent XLV. Its estimated return is 6.56 percent, estimated volatility is 5.27 percent, and reserve weight is 65 percent.",
"This did not make me call the process ready to adopt. The calendar-year-loss rule is still not operationalized by the CIO. I do not silently invent a definition for that rule."
]),
('Point in time evidence',[
"LLY is my company context signal. Its close on November 16, 2026 was 1,431 dollars and 67 cents. I use it only after that market close, and I do not put LLY into the optimizer.",
"The fund estimates come from the saved monthly adjusted-close file through October 19, 2026. I show that different date boundary clearly instead of suggesting that every input updates at the same time."
]),
('One AI-assisted output I checked',[
"AI helped organize the app and documentation, but I checked the calculation path. The program changes adjacent monthly adjusted closes into monthly returns, annualizes the average return and sample volatility, computes correlations, and tests every long-only 5 percent mix.",
"I verified that equal weight fails the return rule, that the 60/40 reference fails the reserve rule, and that the constrained mix passes both checkable rules. Those checks are in the project test file."
]),
('Close',[
"My research evolved from asking which portfolio looks best to asking whether a committee can see the tradeoffs, data dates, and unresolved governance issue. That is why my decision is pilot, not adopt."
])
])
make('Video_2_Code_and_Validation_Transcript.docx','Video 2 Code and Validation', 'Walk through the code that produces the decision and the checks that protect it.', [
('Opening',common_open),
('Show the README and run command',[
"I start in the README. The one command that creates the visible result is python run_analysis dot py. It writes output slash model-output dot md, so a reviewer can read the decision without starting the web app.",
"The interactive version runs with streamlit run app dot py. The tests run with python minus m unittest minus v test_project2 dot py."
]),
('Walk through the calculation code',[
"In portfolio dot py, load_estimates reads the saved monthly adjusted-close data. It calculates each month-to-month return for BIL, IEF, LQD, VTI, and XLV.",
"The same function annualizes the average monthly return by multiplying by 12. It annualizes sample volatility using the square root of 12. It also calculates the correlation table from those monthly return series.",
"The evaluate function takes a proposed set of weights. It calculates expected return, portfolio volatility with the correlation terms, and reserve weight in BIL and IEF.",
"The verdict function checks the return objective and the reserve minimum separately. This matters because a portfolio can pass one rule and fail another.",
"The optimize function tests every long-only 5 percent combination. It discards a mix that misses either checkable rule and keeps the feasible mix with the lowest estimated volatility."
]),
('Show validation',[
"The first validation check shows that equal weight fails the return objective. The second shows that the 60 percent VTI and 40 percent LQD reference fails the reserve minimum. The third shows that the constrained answer passes.",
"For the stress, I increased the objective from 6.5 percent to 7.5 percent. Before the run, the documented expected direction was more equity or no feasible result, and higher estimated volatility if there was a feasible result.",
"The actual stressed portfolio was 50 percent BIL, 35 percent VTI, and 15 percent XLV. Its estimated volatility increased from 5.27 percent to 7.07 percent. The direction matched, but this is sensitivity evidence, not a forecast."
]),
('Limit and close',[
"The code does not pretend to test the calendar-year-loss rule because the CIO did not give a return definition, observation point, or breach response. That is a governance decision, not a missing line of code.",
"The app is reproducible, the output is visible, and the limitations are explicit. Those are the reasons I can pilot the process but not adopt it."
])
])
make('Video_3_Committee_Presentation_Transcript.docx','Video 3 Committee Presentation', 'Open with the live app and deliver a direct committee recommendation.', [
('Opening with the app',[
"Hello. I am opening with the Meridian Reserve Decision Desk running live. My recommendation is pilot, not adopt.",
"This tool is an educational analysis, not investment advice. It is designed to make the mandate verdict, the assumptions, and the decision limits visible to a committee."
]),
('Committee recommendation',[
"The process selects the lowest estimated-volatility long-only portfolio that reaches a 6.5 percent estimated annual return and keeps at least 3 percent in BIL or IEF reserve assets.",
"The current constrained result is 65 percent BIL, 30 percent VTI, and 5 percent XLV. It has a 6.56 percent estimated annual return, 5.27 percent estimated volatility, and 65 percent reserve. It passes the checkable mandate rules.",
"The two baselines explain why the selected portfolio is not just a picked answer. Equal weight has enough reserve but misses the return objective. The 60/40 VTI and LQD reference meets the return objective but fails the reserve rule because it has no reserve assets."
]),
('Risk and data defense',[
"The most important limitation is estimation risk. The return, volatility, and correlation inputs come from historical monthly adjusted-close data. They are estimates, not promises about the future.",
"The LLY close is a separate context signal. LLY closed at 1,431 dollars and 67 cents on November 16, 2026. It is only used after the close and is not an optimizer sleeve.",
"The biggest governance gap is the calendar-year-loss rule. It has a 10 percent limit but no agreed measurement convention or breach action. I will not label that rule as passed until the CIO makes it testable."
]),
('Stress and reversal trigger',[
"I stressed the return objective from 6.5 percent to 7.5 percent. The result shifted toward more equity and estimated volatility rose to 7.07 percent. The recommendation did not change because the governance condition is still unmet.",
"I would stop the process if there is no feasible mix, a checkable mandate rule fails, the point-in-time data convention cannot be defended, or the CIO declines to define the loss rule.",
"I would move from pilot to adopt only after the CIO defines the loss metric, observation date, and breach response, and the process remains feasible through documented data and estimate stresses."
]),
('Close',[
"My request is approval for a paper pilot, not live capital. The pilot would preserve each input date, show its baseline comparisons, rerun the stress checks, and return to the committee if any stop condition occurs. Thank you."
])
])

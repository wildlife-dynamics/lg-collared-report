"""
Generate the LG Collared Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: lg_collared_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "lg_collared_report_technical_guide.pdf"

# ── Colour palette (same as STE Mapbook) ─────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=24, leading=30, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=12, leading=16, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=14, leading=18, textColor=GREEN_DARK,
                  spaceBefore=16, spaceAfter=5, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=11, leading=15, textColor=GREEN_MID,
                  spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=9.5, leading=13, textColor=SLATE,
                  spaceBefore=7, spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=13, textColor=SLATE,
                  spaceAfter=2, leftIndent=14, firstLineIndent=-10)
CELL     = _style("Cell", fontSize=8.5, leading=12, textColor=SLATE,
                  spaceAfter=0, spaceBefore=0)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):       return Paragraph(text, style)
def h1(text):                  return Paragraph(text, H1)
def h2(text):                  return Paragraph(text, H2)
def h3(text):                  return Paragraph(text, H3)
def sp(n=6):                   return Spacer(1, n)
def bullet(text):              return Paragraph(f"• {text}", BULLET)
def note(text):                return Paragraph(f"<b>Note:</b> {text}", NOTE)
def c(text):                   return Paragraph(text, CELL)   # table cell paragraph


def make_table(data, col_widths):
    """Build a table where every cell value is already a Paragraph (use c())."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  GREEN_DARK),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",           (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "LG Collared Report — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="LG Collared Report — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("Lion Guardians Collared Report", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Collared Lion Movement Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"), hr(),
        p(
            "The <b>LG Collared Report</b> workflow analyses GPS-collared lion movement "
            "in the Amboseli ecosystem for the <b>Lion Guardians</b> programme. "
            "It ingests telemetry from <b>EarthRanger</b>, computes home range and track "
            "maps per subject, generates speed and distance statistics, and delivers an "
            "interactive dashboard plus a print-ready Word report."
        ),
        note(
            "All per-group outputs (maps, metrics, Word sections) are produced by iterating "
            "over a user-chosen grouper: subject name, sex, or subtype."
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All telemetry is fetched from an <b>EarthRanger</b> instance via "
            "<code>set_er_connection</code>. The workflow calls "
            "<code>get_subjectgroup_observations</code> once over the configured time range. "
            "The <code>filter: clean</code> parameter discards junk-flagged observations "
            "before they reach the workflow."
        ),

        sp(4), h2("2.2 Groupers"),
        p("Three grouper fields are available via <code>set_groupers</code>:"),
        make_table(
            [
                [c("Grouper field"),   c("EarthRanger source"),      c("Typical use")],
                [c("subject_name"),    c("subject.name"),             c("One output per individual collared lion (default)")],
                [c("subject_sex"),     c("subject.sex"),              c("Aggregate by sex (M / F)")],
                [c("subject_subtype"), c("subject.subject_subtype"),  c("Aggregate by subtype")],
            ],
            [3.8*cm, 4.5*cm, 8.2*cm],
        ),

        sp(6), h2("2.3 Static Geodata Files"),
        p("Three boundary datasets are downloaded from Dropbox and cached locally:"),
        make_table(
            [
                [c("Dataset"),                       c("File"),                          c("Purpose")],
                [c("Group Ranch Boundaries"),        c("lg_group_ranch_boundaries.gpkg"), c("Community ranch polygons in Amboseli")],
                [c("Conflict Hotspot Areas"),        c("lg_conflict_hotspots.gpkg"),      c("Known human–lion conflict hotspot features")],
                [c("Protected Areas"),               c("lg_protected_areas.gpkg"),        c("National parks and reserves")],
            ],
            [4*cm, 5*cm, 7.5*cm],
        ),
        sp(4),
        p(
            "All three files use <code>overwrite_existing: false</code> (3 retries). "
            "After loading, each is reprojected to <b>EPSG:4326</b> and annotated with "
            "its geometry type before layer creation."
        ),

        sp(4), h2("2.4 Word Document Templates"),
        make_table(
            [
                [c("Template file"),                       c("Purpose")],
                [c("collared_lions_cover_page.docx"),      c("Report cover page — subject count, time range, preparer")],
                [c("collared_lion_subject_template.docx"), c("Per-grouper section — metrics and map images")],
            ],
            [6.5*cm, 10*cm],
        ),

        sp(6), h2("2.5 Base Map Tile Layers"),
        make_table(
            [
                [c("Layer"),                   c("Opacity"), c("Max zoom")],
                [c("ArcGIS World Hillshade"),   c("100 %"),   c("20")],
                [c("ArcGIS World Street Map"),  c("15 %"),    c("20")],
            ],
            [10*cm, 2.5*cm, 4*cm],
        ),
        sp(4),
        p(
            "The hillshade provides full-opacity terrain context. "
            "The street map is overlaid at 15 % to show road networks and "
            "settlement names without obscuring the hillshade or data layers."
        ),
    ]

    # ── 3. Data Ingestion ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Observations → Relocations"),
        p(
            "<code>process_relocations</code> converts raw EarthRanger observations to a "
            "standardised GeoDataFrame. Retained columns:"
        ),
        make_table(
            [
                [c("Column"),                         c("Source field"),           c("Description")],
                [c("groupby_col"),                    c("internal"),               c("Subject identifier for grouping")],
                [c("fixtime"),                        c("observation timestamp"),  c("UTC datetime of the GPS fix")],
                [c("junk_status"),                    c("EarthRanger flag"),       c("True if fix is marked junk")],
                [c("geometry"),                       c("lat/lon"),                c("Point geometry (WGS 84)")],
                [c("extra__subject__name"),           c("subject.name"),           c("Lion display name")],
                [c("extra__subject__subject_subtype"),c("subject.subject_subtype"),c("Subject subtype")],
                [c("extra__subject__sex"),            c("subject.sex"),            c("Subject sex (M / F / unknown)")],
            ],
            [4.5*cm, 3.8*cm, 8.2*cm],
        ),
        sp(4),
        p("Three bad coordinate pairs are removed unconditionally:"),
        bullet("(180.0, 90.0) — boundary sentinel"),
        bullet("(0.0, 0.0) — null-island artefact"),
        bullet("(1.0, 1.0) — common default / test value"),
        p("Cleaned relocations are persisted as <code>relocations.geoparquet</code>."),

        sp(4), h2("3.2 Relocations → Trajectories"),
        p(
            "<code>relocations_to_trajectory</code> connects consecutive fixes per subject "
            "into LineString segments, adding <code>dist_meters</code>, "
            "<code>speed_kmhr</code>, <code>segment_start</code>, and "
            "<code>segment_end</code>. Trajectories are persisted as "
            "<code>trajectories.geoparquet</code>."
        ),

        sp(4), h2("3.3 Temporal Index &amp; Speed Classification"),
        p(
            "<code>add_temporal_index</code> keys the trajectory GeoDataFrame to "
            "<code>segment_start</code>, grouped by the configured groupers, enabling "
            "per-group iteration. <code>apply_classification</code> then bins "
            "<code>speed_kmhr</code> into <b>6 equal-interval classes</b> "
            "(output column: <code>speed_bins</code>, labels to 1 decimal place)."
        ),

        sp(4), h2("3.4 Column Renaming &amp; Group Splitting"),
        p(
            "Three columns are renamed via <code>map_columns</code> "
            "(<code>raise_if_not_found: true</code>):"
        ),
        make_table(
            [
                [c("Original column"),         c("Renamed to")],
                [c("extra__name"),             c("subject_name")],
                [c("extra__sex"),              c("subject_sex")],
                [c("extra__subject_subtype"),  c("subject_subtype")],
            ],
            [7.5*cm, 9*cm],
        ),
        sp(4),
        p(
            "The renamed GeoDataFrame is split into per-group partitions by "
            "<code>split_groups</code>. All downstream map and metric tasks iterate "
            "over these partitions via <code>mapvalues</code>."
        ),
    ]

    # ── 4. Static Map Layers ──────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Static Map Layers"), hr(),
        p(
            "Four static layers are built once and composited onto every subject-level map "
            "to provide spatial context."
        ),

        h2("4.1 Layer Styles"),
        make_table(
            [
                [c("Layer"),             c("Colour (RGB)"),       c("Opacity"), c("Filled"), c("Notes")],
                [c("Group Ranch Boundaries"), c("(169, 169, 169) grey"),  c("55 %"), c("No"),
                 c("Outline only, line width 4.5")],
                [c("Conflict Hotspots"), c("(220, 20, 60) crimson"), c("75 %"),  c("Yes"),
                 c("Point radius 2.55, line width 1.95")],
                [c("Protected Areas"),   c("(77, 102, 0) dark green"), c("35 %"), c("Yes"),
                 c("Line width 1.95")],
                [c("Hotspot Text Labels"), c("(20, 20, 20) near-black"), c("—"),  c("—"),
                 c("Arial, 1 000 m base, 40–75 px clamp, centroid-anchored")],
            ],
            [3.8*cm, 3.8*cm, 2*cm, 1.8*cm, 5.1*cm],
        ),
    ]

    # ── 5. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Map Outputs — Methodology"), hr(),

        h2("5.1 Home Range Map (Elliptical Time Density)"),
        p(
            "<code>calculate_elliptical_time_density</code> computes an ETD kernel "
            "density estimate per group, accounting for temporal autocorrelation in "
            "GPS telemetry. Parameters:"
        ),
        make_table(
            [
                [c("Parameter"),    c("Value"),       c("Meaning")],
                [c("CRS"),          c("ESRI:53042"),  c("World Azimuthal Equidistant — equal-area, minimises distortion")],
                [c("percentiles"),  c("50, 60, 70, 80, 90, 95, 99"), c("Contour probability thresholds extracted as polygons")],
                [c("band_count"),   c("1"),           c("Single density band output")],
                [c("nodata_value"), c("NaN"),         c("Cells outside probability mass are transparent")],
            ],
            [3*cm, 4*cm, 9.5*cm],
        ),
        sp(4),
        p(
            "Contour polygons are coloured with the <b>RdYlGn</b> diverging colormap "
            "(innermost 50th percentile = red, outermost 99th = green). "
            "Map opacity is 55 %, legend title: <i>Home Range Percentiles</i>."
        ),
        p(
            "The map view is auto-zoomed via <code>envelope_gdf</code> + "
            "<code>custom_view_state_from_gdf</code> (pitch 0, bearing 0, max zoom 20). "
            "An interactive HTML is persisted (suffix: <code>homerange</code>) then "
            "converted to PNG via <code>adjust_map_zoom_and_screenshot</code> "
            "(2× device scale factor, 40 s tile-load wait)."
        ),

        sp(4), h2("5.2 Subject Tracks Map"),
        p(
            "<code>create_path_layer</code> renders all trajectory segments per group "
            "as a continuous blue path layer:"
        ),
        make_table(
            [
                [c("Property"),       c("Value")],
                [c("Colour"),         c("RGB(0, 0, 255) — blue")],
                [c("Width"),          c("1.55 px, min 2 px, max 8 px (screen-space)")],
                [c("Cap / Join"),     c("Rounded")],
                [c("Opacity"),        c("55 %")],
            ],
            [4.5*cm, 12*cm],
        ),
        sp(4),
        p(
            "The path layer is combined with the four static layers via "
            "<code>combine_deckgl_map_layers</code>. An interactive HTML is persisted "
            "(suffix: <code>tracks</code>) and converted to PNG using the same "
            "screenshot settings as the Home Range map."
        ),
    ]

    # ── 6. Summary Metrics ────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Summary Metrics"), hr(),

        h2("6.1 Per-Group Summary Table"),
        p(
            "<code>summarize_df</code> aggregates trajectory data grouped by "
            "<code>subject_name</code>:"
        ),
        make_table(
            [
                [c("Output column"),  c("Source"),      c("Aggregator"), c("Unit"),    c("D.p.")],
                [c("mean_speed"),     c("speed_kmhr"),  c("mean"),       c("km/h"),    c("2")],
                [c("min_speed"),      c("speed_kmhr"),  c("min"),        c("km/h"),    c("2")],
                [c("max_speed"),      c("speed_kmhr"),  c("max"),        c("km/h"),    c("2")],
                [c("total_distance"), c("dist_meters"), c("sum"),        c("m → km"),  c("2")],
            ],
            [3.5*cm, 3*cm, 2.5*cm, 2.5*cm, 1.5*cm],
        ),
        sp(4),
        p(
            "<code>add_totals_row</code> appends a <i>Total</i> row across all subjects. "
            "The table is persisted as CSV."
        ),

        sp(4), h2("6.2 Scalar Widget Values"),
        p(
            "Four values are derived per group via <code>dataframe_column_sum</code> "
            "then rounded to 2 d.p. by <code>round_off_values</code>:"
        ),
        bullet("Mean Speed (km/h)"),
        bullet("Min Speed (km/h)"),
        bullet("Max Speed (km/h)"),
        bullet("Distance covered (km)"),

        sp(4), h2("6.3 Unique Subject Count"),
        p(
            "<code>dataframe_column_nunique</code> counts distinct values in "
            "<code>groupby_col</code> on the temporally-indexed trajectory GeoDataFrame. "
            "This total is used in the cover page context."
        ),
    ]

    # ── 7. Word Report ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Word Report (.docx)"), hr(),

        h2("7.1 Cover Page"),
        p(
            "<code>create_cl_ctx_cover</code> builds the cover context "
            "(subject count, time range, <i>Ecoscope</i> as preparer). "
            "<code>create_context_page_lg</code> renders it into "
            "<code>lg_cover_page.docx</code>."
        ),

        sp(4), h2("7.2 Per-Grouper Sections"),
        p(
            "<code>create_collared_lions_grouper_ctx</code> assembles a context dict "
            "per group containing the trajectory DataFrame, total distance, Home Range "
            "PNG, and Tracks PNG. <code>create_grouper_page</code> renders each section "
            "from the subject template. Image boxes: <b>11.11 × 6.5 cm</b>. "
            "<code>validate_images: true</code> catches missing PNGs before rendering."
        ),

        sp(4), h2("7.3 Document Merge"),
        p(
            "<code>merge_cl_files</code> concatenates the cover page and all "
            "per-grouper sections into a single Word file saved to the results directory."
        ),
    ]

    # ── 8. Interactive Dashboard ───────────────────────────────────────────────
    story += [
        sp(4), h1("8. Interactive Dashboard"), hr(),
        p(
            "<code>gather_dashboard</code> assembles the <b>Lion Guardians</b> dashboard "
            "from six widget groups:"
        ),
        make_table(
            [
                [c("Widget"),            c("Type"),         c("Source")],
                [c("Mean Speed"),        c("Single value"), c("round_mean_speed → total_mean_speed_sv_widget")],
                [c("Min Speed"),         c("Single value"), c("round_min_speed → total_min_speed_sv_widget")],
                [c("Max Speed"),         c("Single value"), c("round_max_speed → total_max_speed_sv_widget")],
                [c("Distance covered"),  c("Single value"), c("round_total_distance → total_distance_sv_widget")],
                [c("Home Range Metrics"),c("Map"),          c("td_ecomap_html_url → td_grouped_map_widget")],
                [c("Subject tracks"),    c("Map"),          c("track_html_url → sm_grouped_map_widget")],
            ],
            [4.5*cm, 3*cm, 9*cm],
        ),
        sp(4),
        note(
            "Widget tasks use <code>skipif: [never]</code> so the dashboard always "
            "assembles, even when some groups have no data."
        ),
    ]

    # ── 9. Output Files ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("9. Output Files"), hr(),
        p(
            "All files are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."
        ),
        make_table(
            [
                [c("File / pattern"),          c("Format"),     c("Content")],
                [c("relocations.geoparquet"),  c("GeoParquet"), c("Cleaned GPS fix locations")],
                [c("trajectories.geoparquet"), c("GeoParquet"), c("Segments with speed_kmhr, dist_meters, speed_bins")],
                [c("<group>_homerange.html"),  c("HTML"),       c("Interactive ETD home range map")],
                [c("<group>_tracks.html"),     c("HTML"),       c("Interactive subject tracks map")],
                [c("<group>_homerange.png"),   c("PNG"),        c("2× screenshot of home range map")],
                [c("<group>_tracks.png"),      c("PNG"),        c("2× screenshot of tracks map")],
                [c("<group>_summary.csv"),     c("CSV"),        c("Speed and distance summary table with totals row")],
                [c("lg_cover_page.docx"),      c("Word"),       c("Rendered report cover page")],
                [c("<group>.docx"),            c("Word"),       c("Per-grouper report section")],
                [c("<merged_report>.docx"),    c("Word"),       c("Final combined report")],
            ],
            [5*cm, 2.5*cm, 9*cm],
        ),
    ]

    # ── 10. Workflow Execution Logic ──────────────────────────────────────────
    story += [
        sp(4), h1("10. Workflow Execution Logic"), hr(),

        h2("10.1 Skip Conditions"),
        p(
            "Two default skip conditions apply to every task "
            "(<code>task-instance-defaults</code>):"
        ),
        bullet(
            "<b>any_is_empty_df</b> — skips the task (and all dependants) when "
            "any input DataFrame is empty, handling subjects with no fixes gracefully."
        ),
        bullet(
            "<b>any_dependency_skipped</b> — propagates skips downstream automatically."
        ),
        p(
            "Widget and map-widget tasks override this with "
            "<code>skipif: [never]</code> to ensure the dashboard always assembles."
        ),

        sp(4), h2("10.2 Data Flow Summary"),
        make_table(
            [
                [c("Stage"),             c("Tasks")],
                [c("Setup"),             c("EarthRanger connection, time range, groupers, base maps")],
                [c("Geodata download"),  c("3 boundary files + 2 Word templates from Dropbox")],
                [c("Static layers"),     c("Ranch, hotspot, protected area, hotspot text layers")],
                [c("Telemetry ingest"),  c("Observations → relocations → trajectories → speed bins → rename → split")],
                [c("Home Range branch"), c("ETD → colormap → map layer → compose → view state → HTML → PNG → widget")],
                [c("Tracks branch"),     c("Path layer → compose → draw map → HTML → PNG → widget")],
                [c("Metrics branch"),    c("Summary table → totals row → CSV → scalar widget series")],
                [c("Report assembly"),   c("Cover page + per-group sections → merge docx")],
                [c("Dashboard"),         c("gather_dashboard combines all widgets")],
            ],
            [4.5*cm, 12*cm],
        ),
    ]

    # ── 11. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("11. Software Versions"), hr(),
        make_table(
            [
                [c("Package"),                              c("Version"),    c("Role")],
                [c("ecoscope-workflows-core"),              c("0.22.17.*"),  c("Core task library and workflow engine")],
                [c("ecoscope-workflows-ext-ecoscope"),      c("0.22.17.*"),  c("Spatial analysis tasks (ETD, relocations, trajectories)")],
                [c("ecoscope-workflows-ext-custom"),        c("0.0.40.*"),   c("Utility tasks (column mapping, rounding, screenshots)")],
                [c("ecoscope-workflows-ext-ste"),           c("0.0.18.*"),   c("Summary table and totals-row tasks")],
                [c("ecoscope-workflows-ext-mnc"),           c("0.0.7.*"),    c("MNC domain tasks")],
                [c("ecoscope-workflows-ext-big-life"),      c("0.0.8.*"),    c("Big Life Foundation domain tasks")],
                [c("ecoscope-workflows-ext-lion-guardians"),c("0.0.6.*"),    c("Lion Guardians Word report rendering tasks")],
            ],
            [6*cm, 2.5*cm, 8*cm],
        ),
        sp(4),
        p(
            "Packages are distributed via the <code>prefix.dev</code> conda channel "
            "and pinned to patch-compatible versions (<code>.*</code> suffix). "
            "The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()

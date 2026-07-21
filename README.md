# LG Collared Report Workflow

Generates a movement analysis report for GPS-collared lions in the Amboseli ecosystem, sourced from EarthRanger.

## What it produces

The workflow produces, for each collared subject (or group):

- A **Home Range map** (Elliptical Time Density contours at 50&ndash;99th percentiles)
- A **Subject Tracks map** (movement corridors for the analysis period)
- **Speed and distance summary statistics** per subject
- A **Word document report** (`.docx`) with a cover page and one section per subject
- An **interactive dashboard** &mdash; Mean Speed, Min Speed, Max Speed, and Distance Covered (single-value widgets), plus the Home Range and Subject Tracks maps

## Requirements

- Access to an **EarthRanger** instance with a configured data source
- The **Subject Group Name** of the collared lions exactly as it appears in EarthRanger
- The **Conservancies** and **Group Ranch Boundaries** spatial features must exist in that EarthRanger instance &mdash; these are fetched live to build the study-area map layers (no local files or Dropbox boundary downloads are required)

---

## 1. Load the Workflow

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste this repository's URL into the **Github Link** field, then click **Add Template**:

```
https://github.com/wildlife-dynamics/lg-collared-report.git
```

Once added, it appears in the **Workflow Templates** list as **lg-collared-report**. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

---

## 2. Configure the Workflow

### Data Source Connection

Navigate to **Data Sources** and add a new EarthRanger connection. Fill in:

| Field | Description |
|-------|-------------|
| Data Source Name | A label to identify this connection |
| EarthRanger URL | Your instance URL (e.g. `your-site.pamdas.org`) |
| EarthRanger Username | Your EarthRanger username |
| EarthRanger Password | Your EarthRanger password |

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

### Workflow Details

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes about the run (e.g. date range or subject group) |

### Time Range

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the analysis period |
| Until | End date and time of the analysis period |

All movement data, trajectories, and home ranges are computed within this window.

### Basemap Layers

Two stacked ArcGIS tile layers form the background of every map. Pre-filled with sensible defaults, but the URL, opacity, and max zoom of each layer are editable.

| Layer | Default Opacity | Max Zoom |
|-------|------------------|----------|
| ESRI World Hillshade | `1.0` | `15` |
| ESRI World Street Map | `0.15` | `15` |

### Groupers

Groupers control how the workflow partitions subjects for per-group outputs. **Subject Name is pre-selected by default** &mdash; producing one map, metrics table, and report section per individual lion. Click **Add** to change or add groupers:

| Grouper | Effect |
|---------|--------|
| Subject Name | One output per individual collared lion (default) |
| Subject Sex | Aggregate outputs by sex (M / F) |
| Subject Subtype | Aggregate outputs by subtype |

### Connect to EarthRanger

Select the EarthRanger data source configured above from the **Connect to EarthRanger** dropdown.

### Subject Group

Enter the **Subject Group Name** exactly as it appears in EarthRanger (case-sensitive). This is the group of collared lions to include in the report.

> Using a subject group that contains mixed subtypes may produce unexpected results.

### Trajectory Filter

Expand **Advanced Configurations** under **Transform relocations to trajectories** to set the segment filter. These parameters remove GPS noise and biologically unrealistic movements before trajectory analysis.

| Field | Default | Description |
|-------|---------|-------------|
| Minimum Segment Length (m) | `10` | Discard segments shorter than this distance |
| Maximum Segment Length (m) | `10000` | Discard segments longer than this distance |
| Minimum Segment Duration (s) | `10` | Discard segments shorter than this duration |
| Maximum Segment Duration (s) | `21600` | Discard segments longer than this duration (6 hours) |
| Minimum Segment Speed (km/h) | `1` | Discard segments below this average speed |
| Maximum Segment Speed (km/h) | `30` | Discard segments above this average speed |

Adjust these values to suit the movement characteristics of your collared lions.

### Time Density Map and Zoom to Envelope

Expand **Advanced Configurations** under **Time density map** to control the home range computation, and configure the map zoom settings below it.

**Time density map**

| Field | Default | Description |
|-------|---------|-------------|
| Grid Cell Size | `Auto-scale` | Cell size of the density raster &mdash; Auto-scale derives it from data density |
| Max Speed Factor | `1.05` | Estimate of the subject's maximum speed as a factor of the maximum measured speed in the dataset |
| Shape Buffer Expansion Factor | `1.3` | Controls how far time density values spread across the grid, affecting the smoothness of the output |

**Zoom to envelope**

| Field | Default | Description |
|-------|---------|-------------|
| Expansion Factor | `1.00` | Factor to expand the bounding box around the data extent before zooming (e.g. `1.2` = 20% larger) |

A value of `1.0` gives a tight fit to the data; increasing it adds padding around the map extent.

---

## 3. Run the Workflow

Once all parameters are configured, click **Submit**. The runner will:

1. Pull movement data from EarthRanger for the specified subject group and time range.
2. Fetch the Conservancies and Group Ranch Boundaries spatial features from EarthRanger to build the study-area map layers.
3. Convert observations to relocations and build trajectory segments.
4. Compute Elliptical Time Density home ranges per group.
5. Generate the Home Range and Subject Tracks maps (interactive HTML + PNG screenshots).
6. Calculate speed and distance summary statistics per subject.
7. Render the Word report (cover page + per-subject sections) and assemble the dashboard.
8. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

### Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`:

| File | Description |
|------|-------------|
| `relocations.geoparquet` | Cleaned GPS fix locations |
| `trajectories.geoparquet` | Trajectory segments with speed and distance |
| `<group>_homerange.html` | Interactive ETD home range map per group |
| `<group>_tracks.html` | Interactive subject tracks map per group |
| `<group>_homerange.png` | Screenshot of the home range map (2&times; resolution) |
| `<group>_tracks.png` | Screenshot of the tracks map (2&times; resolution) |
| `<group>_summary.csv` | Speed and distance summary table (one row per subject) |
| `cover_page.docx` | Rendered report cover page |
| `<group>.docx` | Per-grouper report section |
| `overall_report.docx` | Final combined Word report |

---

## More Help

- **Technical Guide:** [technical_guide/lg_collared_report_technical_guide.pdf](technical_guide/lg_collared_report_technical_guide.pdf) &mdash; pipeline internals and task-by-task reference
- **Issues:** [github.com/wildlife-dynamics/lg-collared-report/issues](https://github.com/wildlife-dynamics/lg-collared-report/issues)

## Development

This workflow's code (`ecoscope-workflows-collared-report-workflow/`) is generated from [`spec.yaml`](spec.yaml) and [`test-cases.yaml`](test-cases.yaml). After editing either file, recompile and commit the generated changes:

```
pixi run --manifest-path pixi.toml --locked bash -c "./dev/recompile.sh --update"
```

## License

[BSD 3-Clause](LICENSE)

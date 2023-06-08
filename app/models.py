"""Models"""

from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import CHAR, NUMERIC, TEXT


class Base(DeclarativeBase):
    pass

class Batches(Base):
    __tablename__ = "batches"

    batch_name: Mapped[str] = mapped_column(TEXT, primary_key=True)
    min_percent_present_filter: Mapped[Optional[float]] = mapped_column(NUMERIC)
    min_reads_post_filter: Mapped[Optional[int]]
    max_reads_factor: Mapped[Optional[float]] = mapped_column(NUMERIC)
    vector_of_littlem_values: Mapped[Optional[str]] = mapped_column(TEXT)
    vector_of_bigm_values: Mapped[Optional[str]] = mapped_column(TEXT)

class BioProjects(Base):
    __tablename__ = "bioprojects"

    bioproj_acc_id: Mapped[str] = mapped_column(TEXT, primary_key=True)
    project_datathon_index: Mapped[Optional[str]] = mapped_column(TEXT)
    library_selection_sra: Mapped[Optional[str]] = mapped_column(TEXT)
    library_strat_sra: Mapped[Optional[str]] = mapped_column(TEXT)
    read_type_sra: Mapped[Optional[str]] = mapped_column(TEXT)
    sequencing_platform: Mapped[Optional[str]] = mapped_column(TEXT)
    instrument_model: Mapped[Optional[str]] = mapped_column(TEXT)
    study_acc_sra: Mapped[Optional[str]] = mapped_column(TEXT)
    experiment_acc_sra: Mapped[Optional[str]] = mapped_column(TEXT)
    package_biosamp: Mapped[Optional[str]] = mapped_column(TEXT)

class Datasets(Base):
    __tablename__ = "datasets"

    dataset_name: Mapped[str] = mapped_column(TEXT, primary_key=True)
    batch_name: Mapped[str] = mapped_column(TEXT, ForeignKey("batches.batch_name"))
    bioproj_acc_id: Mapped[str] = mapped_column(TEXT, ForeignKey("bioprojects.bioproj_acc_id"))
    r80: Mapped[Optional[str]] = mapped_column(TEXT)


class EventMetadata(Base):
    """
    ORM wrapper for the event_metadata table.
    Excludes the geom column since we don't need it in python.
    """
    __tablename__ = "event_metadata"

    event_id: Mapped[str] = mapped_column(TEXT, primary_key=True)
    collector_list: Mapped[Optional[str]] = mapped_column(TEXT)
    continent_ocean: Mapped[Optional[str]] = mapped_column(TEXT)
    coordinate_uncertainty_in_meters: Mapped[Optional[float]] = mapped_column(NUMERIC)
    country: Mapped[Optional[str]] = mapped_column(TEXT)
    day_collected: Mapped[Optional[int]]
    decimal_latitude: Mapped[Optional[float]] = mapped_column(NUMERIC)
    decimal_longitude: Mapped[Optional[float]] = mapped_column(NUMERIC)
    environmental_medium: Mapped[Optional[str]] = mapped_column(TEXT)
    expedition_code: Mapped[Optional[str]] = mapped_column(TEXT)
    georeference_protocol: Mapped[Optional[str]] = mapped_column(TEXT)
    habitat: Mapped[Optional[str]] = mapped_column(TEXT)
    land_owner: Mapped[Optional[str]] = mapped_column(TEXT)
    locality: Mapped[str] = mapped_column(TEXT)
    maximum_depth_in_meters: Mapped[Optional[float]] = mapped_column(NUMERIC)
    maximum_elevation_in_meters: Mapped[Optional[float]] = mapped_column(NUMERIC)
    microhabitat: Mapped[Optional[str]] = mapped_column(TEXT)
    minimum_depth_in_meters: Mapped[Optional[float]] = mapped_column(NUMERIC)
    minimum_elevation_in_meters: Mapped[Optional[float]] = mapped_column(NUMERIC)
    month_collected: Mapped[Optional[int]]
    permit_information: Mapped[Optional[str]] = mapped_column(TEXT)
    principal_investigator: Mapped[Optional[str]] = mapped_column(TEXT)
    sampling_protocol: Mapped[Optional[str]] = mapped_column(TEXT)
    state_province: Mapped[Optional[str]] = mapped_column(TEXT)
    year_collected: Mapped[int]
    geom = Column(Geometry('POINT'))

class SampleMetadata(Base):
    __tablename__ = "sample_metadata"

    sample_bcid: Mapped[str] = mapped_column(TEXT, primary_key=True)
    event_id: Mapped[str] = mapped_column(TEXT, ForeignKey("event_metadata.event_id")) 
    dataset_name: Mapped[str] = mapped_column(TEXT, ForeignKey("datasets.dataset_name"))
    associated_media: Mapped[Optional[str]] = mapped_column(TEXT)
    associated_references: Mapped[Optional[str]] = mapped_column(TEXT)
    biosample_acc_sra: Mapped[str] = mapped_column(TEXT)
    taxonomic_class: Mapped[Optional[str]] = mapped_column(TEXT, name="class")
    colloquial_name: Mapped[Optional[str]] = mapped_column(TEXT)
    establishment_means: Mapped[Optional[str]] = mapped_column(TEXT)
    family: Mapped[Optional[str]] = mapped_column(TEXT)
    genus: Mapped[Optional[str]] = mapped_column(TEXT)
    infraspecies: Mapped[Optional[str]] = mapped_column(TEXT)
    life_stage: Mapped[Optional[str]] = mapped_column(TEXT)
    material_sample_id: Mapped[str] = mapped_column(TEXT)
    nomenclatural_code: Mapped[Optional[str]] = mapped_column(TEXT)
    other_catalog_numbers: Mapped[Optional[str]] = mapped_column(TEXT)
    phylum: Mapped[Optional[str]] = mapped_column(TEXT)
    preservative: Mapped[Optional[str]] = mapped_column(TEXT)
    principal_investigator: Mapped[Optional[str]] = mapped_column(TEXT)
    run_acc_sra: Mapped[Optional[str]] = mapped_column(TEXT)
    sample_entered_by: Mapped[Optional[str]] = mapped_column(TEXT)
    sex: Mapped[Optional[str]] = mapped_column(TEXT)
    specific_epithet: Mapped[Optional[str]] = mapped_column(TEXT)
    taxonomic_order: Mapped[Optional[str]] = mapped_column(TEXT)
    tissue_type: Mapped[Optional[str]] = mapped_column(TEXT)

class StacksRuns(Base):
    __tablename__ = "stacks_runs"

    stacks_run_id: Mapped[int] = mapped_column(primary_key=True)
    stacks_run_name: Mapped[str] = mapped_column(TEXT)
    dataset_name: Mapped[str] = mapped_column(TEXT, ForeignKey("dataseta.dataset_name"))
    little_m: Mapped[int]
    big_m: Mapped[int]
    n: Mapped[int]

class StacksRunsDerivedData(Base):
    __tablename__ = "stacks_run_derived_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    stacks_run_id: Mapped[int] = mapped_column(ForeignKey("stacks_runs.stacks_run_id"))
    filename: Mapped[str] = mapped_column(TEXT)
    file_type: Mapped[str] = mapped_column(TEXT)

class PopulationHapstats(Base):
    __tablename__ = "population_hapstats"

    id: Mapped[int] = mapped_column(primary_key=True)
    stacks_run_id: Mapped[int] = mapped_column(ForeignKey("stacks_runs.stacks_run_id"))
    locus_id: Mapped[int]
    chr: Mapped[str] = mapped_column(TEXT)
    bp: Mapped[int]
    pop_id: Mapped[str] = mapped_column(TEXT)
    n_inds: Mapped[int]
    haplotype_cnt: Mapped[int]
    gene_diversity: Mapped[float] = mapped_column(NUMERIC)
    smoothed_gene_diversity: Mapped[float] = mapped_column(NUMERIC)
    smoothed_gene_diversity_p_value: Mapped[float] = mapped_column(NUMERIC)
    haplotype_diversity: Mapped[float] = mapped_column(NUMERIC)
    smoothed_haplotype_diversity: Mapped[float] = mapped_column(NUMERIC)
    smoothed_haplotype_diversity_p_value: Mapped[float] = mapped_column(NUMERIC)
    hwe_p_value: Mapped[float] = mapped_column(NUMERIC)
    hwe_p_value_se: Mapped[float] = mapped_column(NUMERIC)
    haplotypes: Mapped[str] = mapped_column(TEXT)

class PopulationsSumStats(Base):
    __tablename__ = "populations_sumstats"

    id: Mapped[int] = mapped_column(primary_key=True)
    stacks_run_id: Mapped[int] = mapped_column(ForeignKey("stacks_runs.stacks_run_id"))
    locus_id: Mapped[int]
    chr: Mapped[str] = mapped_column(TEXT)
    bp: Mapped[int]
    col: Mapped[int]
    pop_id: Mapped[str] = mapped_column(TEXT)
    p_nuc: Mapped[str] = mapped_column(String(1).with_variant(CHAR(1), "postgresql"))
    q_nuc: Mapped[str] = mapped_column(String(1).with_variant(CHAR(1), "postgresql"))
    n_inds: Mapped[int]
    p_freq: Mapped[float] = mapped_column(NUMERIC)
    obs_het: Mapped[float] = mapped_column(NUMERIC)
    obs_hom: Mapped[float] = mapped_column(NUMERIC)
    exp_het: Mapped[float] = mapped_column(NUMERIC)
    exp_hom: Mapped[float] = mapped_column(NUMERIC)
    pi: Mapped[float] = mapped_column(NUMERIC)
    smoothed_pi: Mapped[float] = mapped_column(NUMERIC)
    smoothed_pi_p_value: Mapped[float] = mapped_column(NUMERIC)
    fis: Mapped[float] = mapped_column(NUMERIC)
    smoothed_fis: Mapped[float] = mapped_column(NUMERIC)
    smoothed_fis_p_value: Mapped[float] = mapped_column(NUMERIC)
    hwe_p_value: Mapped[float] = mapped_column(NUMERIC)
    private: Mapped[float] = mapped_column(NUMERIC)

class PopulationsSumStatsSummaryVariantPositions(Base):
    __tablename__ = "populations_sumstats_summary_variant_positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    stacks_run_id: Mapped[int] = mapped_column(ForeignKey("stacks_runs.stacks_run_id"))
    pop_id: Mapped[str] = mapped_column(TEXT)
    private: Mapped[int]
    num_indiv: Mapped[float] = mapped_column(NUMERIC)
    num_indiv_var: Mapped[float] = mapped_column(NUMERIC)
    num_indiv_stderr: Mapped[float] = mapped_column(NUMERIC)
    p: Mapped[float] = mapped_column(NUMERIC)
    p_var: Mapped[float] = mapped_column(NUMERIC)
    p_stderr: Mapped[float] = mapped_column(NUMERIC)
    obs_het: Mapped[float] = mapped_column(NUMERIC)
    obs_het_var: Mapped[float] = mapped_column(NUMERIC)
    obs_het_stderr: Mapped[float] = mapped_column(NUMERIC)
    obs_hom: Mapped[float] = mapped_column(NUMERIC)
    obs_hom_var: Mapped[float] = mapped_column(NUMERIC)
    obs_hom_stderr: Mapped[float] = mapped_column(NUMERIC)
    exp_het: Mapped[float] = mapped_column(NUMERIC)
    exp_het_var: Mapped[float] = mapped_column(NUMERIC)
    exp_het_stderr: Mapped[float] = mapped_column(NUMERIC)
    exp_hom: Mapped[float] = mapped_column(NUMERIC)
    exp_hom_var: Mapped[float] = mapped_column(NUMERIC)
    exp_hom_stderr: Mapped[float] = mapped_column(NUMERIC)
    pi: Mapped[float] = mapped_column(NUMERIC)
    pi_var: Mapped[float] = mapped_column(NUMERIC)
    pi_stderr: Mapped[float] = mapped_column(NUMERIC)
    fis: Mapped[float] = mapped_column(NUMERIC)
    fis_var: Mapped[float] = mapped_column(NUMERIC)
    fix_stderr: Mapped[float] = mapped_column(NUMERIC)

class PopulationsSumStatsSummaryAllPositions(Base):
    __tablename__ = "populations_sumstats_summary_all_positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    stacks_run_id: Mapped[int] = mapped_column(ForeignKey("stacks_runs.stacks_run_id"))
    pop_id: Mapped[str] = mapped_column(TEXT)
    private: Mapped[int]
    sites: Mapped[int]
    variant_sites: Mapped[int]
    polymorphic_sites: Mapped[int]
    percent_polymorphic_loci: Mapped[float] = mapped_column(NUMERIC)
    num_indiv: Mapped[float] = mapped_column(NUMERIC)
    num_indiv_var: Mapped[float] = mapped_column(NUMERIC)
    num_indiv_stderr: Mapped[float] = mapped_column(NUMERIC)
    p: Mapped[float] = mapped_column(NUMERIC)
    p_var: Mapped[float] = mapped_column(NUMERIC)
    p_stderr: Mapped[float] = mapped_column(NUMERIC)
    obs_het: Mapped[float] = mapped_column(NUMERIC)
    obs_het_var: Mapped[float] = mapped_column(NUMERIC)
    obs_het_stderr: Mapped[float] = mapped_column(NUMERIC)
    obs_hom: Mapped[float] = mapped_column(NUMERIC)
    obs_hom_var: Mapped[float] = mapped_column(NUMERIC)
    obs_hom_stderr: Mapped[float] = mapped_column(NUMERIC)
    exp_het: Mapped[float] = mapped_column(NUMERIC)
    exp_het_var: Mapped[float] = mapped_column(NUMERIC)
    exp_het_stderr: Mapped[float] = mapped_column(NUMERIC)
    exp_hom: Mapped[float] = mapped_column(NUMERIC)
    exp_hom_var: Mapped[float] = mapped_column(NUMERIC)
    exp_hom_stderr: Mapped[float] = mapped_column(NUMERIC)
    pi: Mapped[float] = mapped_column(NUMERIC)
    pi_var: Mapped[float] = mapped_column(NUMERIC)
    pi_stderr: Mapped[float] = mapped_column(NUMERIC)
    fis: Mapped[float] = mapped_column(NUMERIC)
    fis_var: Mapped[float] = mapped_column(NUMERIC)
    fix_stderr: Mapped[float] = mapped_column(NUMERIC)
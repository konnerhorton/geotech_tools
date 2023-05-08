import pandas as pd
import numpy as np


def calculate_particle_size_distribution_general(particle_size, percentage_passing):
    """
    Accepts two lists of equal length. Returns dictionary of particle size percentages.

    :param particle_size: list, particle size measurements
    :param percentage_passing: list, percent passing at each particle size

    :return particle_size_analysis: dict, summarizing gravel, sand, silt, and clay percentages in sample
    """

    particle_size_analysis = {
        "Gravel": {
            "Boundary": 4.75,
            "Percentage Passing": None,
            "Percentage Contained": None,
        },
        "Sand": {
            "Boundary": 0.75,
            "Percentage Passing": None,
            "Percentage Contained": None,
        },
        "Silt": {
            "Boundary": 0.05,
            "Percentage Passing": None,
            "Percentage Contained": None,
        },
        "Clay": {
            "Boundary": 0.002,
            "Percentage Passing": None,
            "Percentage Contained": None,
        },
    }

    particle_size_boundaries = [
        v["Boundary"] for k, v in particle_size_analysis.items()
    ]

    print(particle_size_boundaries)

    # use Numpy to performa a linear interpolation at each particle size boundary value
    percentage_passing_at_boundaries = np.interp(
        particle_size_boundaries, particle_size, percentage_passing
    )

    # the list from the interpolation is the percent passing, convert this to percent retained
    # list order: [gravel, sand, silt, clay]

    # Gravel
    particle_size_analysis["Gravel"][
        "Percentage Passing"
    ] = percentage_passing_at_boundaries[0]

    particle_size_analysis["Gravel"]["Percentage Contained"] = (
        100 - percentage_passing_at_boundaries[0]
    )

    # Clay
    particle_size_analysis["Clay"][
        "Percentage Passing"
    ] = percentage_passing_at_boundaries[3]

    particle_size_analysis["Clay"][
        "Percentage Contained"
    ] = percentage_passing_at_boundaries[3]

    # Silt
    particle_size_analysis["Silt"][
        "Percentage Passing"
    ] = percentage_passing_at_boundaries[2]

    particle_size_analysis["Silt"]["Percentage Contained"] = (
        particle_size_analysis["Silt"]["Percentage Passing"]
        - particle_size_analysis["Clay"]["Percentage Contained"]
    )

    # Sand
    particle_size_analysis["Sand"][
        "Percentage Passing"
    ] = percentage_passing_at_boundaries[1]

    particle_size_analysis["Sand"]["Percentage Contained"] = 100 - (
        particle_size_analysis["Clay"]["Percentage Contained"]
        + particle_size_analysis["Silt"]["Percentage Contained"]
        + particle_size_analysis["Gravel"]["Percentage Contained"]
    )

    # round calculated values
    for k, v in particle_size_analysis.items():
        for l, w in v.items():
            if l in ["Percentage Passing", "Percentage Contained"]:
                v[l] = round(w, 1)

    return particle_size_analysis

import pandas as pd
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import csv
import asyncio
import aiohttp
import click
import ast
import numpy as np
import json
import shkim219.query
import os
pd.options.mode.chained_assignment = None  # default='warn'


headers = {'Authorization': 'eyJhbGciOiJSUzI1NiJ9.eyJoeXBpLmxvZ2luIjp0cnVlLCJoeXBpLnVzZXJuYW1lIjoic2hraW0yMTlAYnUuZWR1IiwiaHlwaS5lbWFpbCI6InNoa2ltMjE5QGJ1LmVkdSIsImF1ZCI6IjAxRjdWNDE3MFpERFNFWUY4OFZaVDVaNEdGIiwiaWF0IjoxNjI2MTAxNzU2LCJleHAiOjE2Mjg2OTM3NTYsInN1YiI6IjAxRjdWNDE3MFo0R0NDWllSNVcyTTBKUTA0IiwibmJmIjoxNjI2MTAxNzU2fQ.FEw4oK6yaVSZUukvdPES7RqvmaFyTJZpUVxqDnhcdLwsLaosni5dJn0FTjNURt_rMuqfgpz4ijWJ18od7q1GhcOjfPodtUJjM_uv0j3LUcA0DYX9_MKw0LGjlhfK93t2h8zCMXQUfkjjB2ZYPObHkBteshlswtJDhP39q1jQzLHu0ElnYTrM1ZrQ33SfbTbX6QsVzhIEky-rkgkcoVan9_RDfNNrI6GqMsGFp1clWS7dZSROEMIWpe_1mEXWo2xBepJ0ixzEjeOyunnRhihzRQFV-3JrXgK9Skg1O944DOqvyKDDJ-fd7V7qNPTKLV6mNUwO2L3c4KR7YdE_9ERwtA',
           'hypi-domain': 'dismembered.apps.hypi.app'}

transport = AIOHTTPTransport(url='https://api.hypi.app/graphql', headers=headers)
client = Client(transport=transport, fetch_schema_from_transport=True)


# def retrievecells(filename):
#     fieldnames = ['area', 'bounding_box_area', 'bounding_box_maximum_column', 'bounding_box_maximum_row', 'bounding_box_minimum_column', 'bounding_box_minimum_row', 'centroid_column', 'centroid_row', 'centroid_weighted_column',
#                   'centroid_weighted_local_column', 'centroid_weighted_local_row', 'centroid_weighted_row', 'convex_hull_area', 'eccentricity', 'equivalent_diameter', 'euler_number', 'extent', 'inertia_tensor_0_0', 'inertia_tensor_0_1',
#                   'inertia_tensor_1_0', 'inertia_tensor_1_1', 'inertia_tensor_eigen_values_0', 'inertia_tensor_eigen_values_1', 'intensity_integrated', 'intensity_maximum', 'intensity_mean', 'intensity_median', 'intensity_median_absolute_deviation',
#                   'intensity_minimum', 'intensity_quartile_1', 'intensity_quartile_2', 'intensity_quartile_3', 'intensity_standard_deviation', 'label', 'major_axis_length', 'minor_axis_length', 'moments_central_0_0', 'moments_central_0_1',
#                   'moments_central_0_2', 'moments_central_1_0', 'moments_central_1_1', 'moments_central_1_2', 'moments_central_2_0', 'moments_central_2_1', 'moments_central_2_2', 'moments_hu_0', 'moments_hu_1', 'moments_hu_2', 'moments_hu_3',
#                   'moments_hu_4', 'moments_hu_5', 'moments_hu_6', 'moments_hu_weighted_0', 'moments_hu_weighted_1', 'moments_hu_weighted_2', 'moments_hu_weighted_3', 'moments_hu_weighted_4', 'moments_hu_weighted_5', 'moments_hu_weighted_6',
#                   'moments_normalized_0_0', 'moments_normalized_0_1', 'moments_normalized_0_2', 'moments_normalized_1_0', 'moments_normalized_1_1', 'moments_normalized_1_2', 'moments_normalized_2_0', 'moments_normalized_2_1', 'moments_normalized_2_2',
#                   'moments_spatial_0_0', 'moments_spatial_0_1', 'moments_spatial_0_2', 'moments_spatial_1_0', 'moments_spatial_1_1', 'moments_spatial_1_2', 'moments_spatial_2_0', 'moments_spatial_2_1', 'moments_spatial_2_2', 'moments_weighted_central_0_0',
#                   'moments_weighted_central_0_1', 'moments_weighted_central_0_2', 'moments_weighted_central_1_0', 'moments_weighted_central_1_1', 'moments_weighted_central_1_2', 'moments_weighted_central_2_0', 'moments_weighted_central_2_1',
#                   'moments_weighted_central_2_2', 'moments_weighted_normalized_0_0', 'moments_weighted_normalized_0_1', 'moments_weighted_normalized_0_2', 'moments_weighted_normalized_1_0', 'moments_weighted_normalized_1_1', 'moments_weighted_normalized_1_2',
#                   'moments_weighted_normalized_2_0', 'moments_weighted_normalized_2_1', 'moments_weighted_normalized_2_2', 'moments_weighted_spatial_0_0', 'moments_weighted_spatial_0_1', 'moments_weighted_spatial_0_2', 'moments_weighted_spatial_1_0',
#                   'moments_weighted_spatial_1_1', 'moments_weighted_spatial_1_2', 'moments_weighted_spatial_2_0', 'moments_weighted_spatial_2_1', 'moments_weighted_spatial_2_2', 'orientation', 'perimeter', 'shannon_entropy_hartley', 'shannon_entropy_natural',
#                   'shannon_entropy_shannon', 'solidity', 'moments_zernike_8_8_00', 'moments_zernike_8_8_01', 'moments_zernike_8_8_02', 'moments_zernike_8_8_03', 'moments_zernike_8_8_04', 'moments_zernike_8_8_05', 'moments_zernike_8_8_06', 'moments_zernike_8_8_07',
#                   'moments_zernike_8_8_08', 'moments_zernike_8_8_09', 'moments_zernike_8_8_10', 'moments_zernike_8_8_11', 'moments_zernike_8_8_12', 'moments_zernike_8_8_13', 'moments_zernike_8_8_14', 'moments_zernike_8_8_15', 'moments_zernike_8_8_16',
#                   'moments_zernike_8_8_17', 'moments_zernike_8_8_18', 'moments_zernike_8_8_19', 'moments_zernike_8_8_20', 'moments_zernike_8_8_21', 'moments_zernike_8_8_22', 'moments_zernike_8_8_23', 'moments_zernike_8_8_24', 'threshold_adjacency_statistics_00',
#                   'threshold_adjacency_statistics_01', 'threshold_adjacency_statistics_02', 'threshold_adjacency_statistics_03', 'threshold_adjacency_statistics_04', 'threshold_adjacency_statistics_05', 'threshold_adjacency_statistics_06',
#                   'threshold_adjacency_statistics_07', 'threshold_adjacency_statistics_08', 'threshold_adjacency_statistics_09', 'threshold_adjacency_statistics_10', 'threshold_adjacency_statistics_11', 'threshold_adjacency_statistics_12',
#                   'threshold_adjacency_statistics_13', 'threshold_adjacency_statistics_14', 'threshold_adjacency_statistics_15', 'threshold_adjacency_statistics_16', 'threshold_adjacency_statistics_17', 'threshold_adjacency_statistics_18',
#                   'threshold_adjacency_statistics_19', 'threshold_adjacency_statistics_20', 'threshold_adjacency_statistics_21', 'threshold_adjacency_statistics_22', 'threshold_adjacency_statistics_23', 'threshold_adjacency_statistics_24',
#                   'threshold_adjacency_statistics_25', 'threshold_adjacency_statistics_26', 'threshold_adjacency_statistics_27', 'threshold_adjacency_statistics_28', 'threshold_adjacency_statistics_29', 'threshold_adjacency_statistics_30',
#                   'threshold_adjacency_statistics_31', 'threshold_adjacency_statistics_32', 'threshold_adjacency_statistics_33', 'threshold_adjacency_statistics_34', 'threshold_adjacency_statistics_35', 'threshold_adjacency_statistics_36',
#                   'threshold_adjacency_statistics_37', 'threshold_adjacency_statistics_38', 'threshold_adjacency_statistics_39', 'threshold_adjacency_statistics_40', 'threshold_adjacency_statistics_41', 'threshold_adjacency_statistics_42',
#                   'threshold_adjacency_statistics_43', 'threshold_adjacency_statistics_44', 'threshold_adjacency_statistics_45', 'threshold_adjacency_statistics_46', 'threshold_adjacency_statistics_47', 'threshold_adjacency_statistics_48',
#                   'threshold_adjacency_statistics_49', 'threshold_adjacency_statistics_50', 'threshold_adjacency_statistics_51', 'threshold_adjacency_statistics_52', 'threshold_adjacency_statistics_53', 'local_binary_patterns_00_08_06',
#                   'local_binary_patterns_01_08_06', 'local_binary_patterns_02_08_06', 'local_binary_patterns_03_08_06', 'local_binary_patterns_04_08_06', 'local_binary_patterns_05_08_06', 'local_binary_patterns_06_08_06', 'local_binary_patterns_07_08_06',
#                   'local_binary_patterns_08_08_06', 'local_binary_patterns_09_08_06', 'local_binary_patterns_10_08_06', 'local_binary_patterns_11_08_06', 'local_binary_patterns_12_08_06', 'local_binary_patterns_13_08_06', 'haralick_angular_second_moment_8_000',
#                   'haralick_contrast_8_000', 'haralick_correlation_8_000', 'haralick_sum_of_squares_variance_8_000', 'haralick_inverse_difference_moment_8_000', 'haralick_sum_average_8_000', 'haralick_sum_variance_8_000', 'haralick_sum_entropy_8_000',
#                   'haralick_entropy_8_000', 'haralick_difference_variance_8_000', 'haralick_difference_entropy_8_000', 'haralick_information_measure_of_correlation_1_8_000', 'haralick_information_measure_of_correlation_2_8_000',
#                   'haralick_angular_second_moment_8_090', 'haralick_contrast_8_090', 'haralick_correlation_8_090', 'haralick_sum_of_squares_variance_8_090', 'haralick_inverse_difference_moment_8_090', 'haralick_sum_average_8_090', 'haralick_sum_variance_8_090',
#                   'haralick_sum_entropy_8_090', 'haralick_entropy_8_090', 'haralick_difference_variance_8_090', 'haralick_difference_entropy_8_090', 'haralick_information_measure_of_correlation_1_8_090', 'haralick_information_measure_of_correlation_2_8_090',
#                   'haralick_angular_second_moment_8_180', 'haralick_contrast_8_180', 'haralick_correlation_8_180', 'haralick_sum_of_squares_variance_8_180', 'haralick_inverse_difference_moment_8_180', 'haralick_sum_average_8_180', 'haralick_sum_variance_8_180',
#                   'haralick_sum_entropy_8_180', 'haralick_entropy_8_180', 'haralick_difference_variance_8_180', 'haralick_difference_entropy_8_180', 'haralick_information_measure_of_correlation_1_8_180', 'haralick_information_measure_of_correlation_2_8_180',
#                   'haralick_angular_second_moment_8_270', 'haralick_contrast_8_270', 'haralick_correlation_8_270', 'haralick_sum_of_squares_variance_8_270', 'haralick_inverse_difference_moment_8_270', 'haralick_sum_average_8_270', 'haralick_sum_variance_8_270',
#                   'haralick_sum_entropy_8_270', 'haralick_entropy_8_270', 'haralick_difference_variance_8_270', 'haralick_difference_entropy_8_270', 'haralick_information_measure_of_correlation_1_8_270', 'haralick_information_measure_of_correlation_2_8_270',
#                   'pathname']
#     cellarray = shkim219.query.retrievecells(filename)
#     return np.concatenate(fieldnames, cellarray)


def create_cell(file, style):
    df = pd.read_csv(file)
    df.dropna(how="all", inplace=True)
    for i in range(len(df)):
        createcell((i+1), df.iloc[i], file, style)

def createcell(no, arr, filename, style):
    s = str(no)
    slashloc = str(filename).rfind("/")
    if(slashloc == -1):
        slashloc = str(filename).rfind("\\")
    csvloc = str(filename).rfind(".csv")
    filenamestr = str(filename)[slashloc+1:csvloc+4]
    finalid = filenamestr + s
    print(finalid)
    if(style == "kmeans"):
        celltype = one_cell_kmeans(arr, finalid)
    query = gql(
        """
        mutation AddCells {
          upsert(values:{
            Cell:[
              {
                """
        + celltype +
        """   }
      ],
      Filename: [
      {
        hypi: {id: \"""" + filenamestr + """\"},
        csvname: \"""" + filenamestr + """\",
        totalnumber: """ + s + """
      }
      ]
    }){id}
  }
"""
    )
    return client.execute(query)

def one_cell_kmeans(arr, id):
    for i in range(len(arr)):
        if str(arr[i]) == 'nan':
            arr[i] = " "
    # print(len(arr))
    area = arr[0]
    bound = arr[1:6]
    centroid = arr[6:12]
    convex_hull_area = arr[12]
    eccentricity = arr[13]
    equivalent_diameter = arr[14]
    euler_number = arr[15]
    extent = arr[16]
    inertia = arr[17:23]
    intensity = arr[23:33]
    label = arr[33]
    major_axis = arr[34]
    minor_axis = arr[35]
    moments = arr[36:104]
    orientation = arr[104]
    perimeter = arr[105]
    shannon_entropy = arr[106:109]
    solidity = arr[109]
    moments_zernike = arr[110:135]
    threshold_adjacency_statistics = arr[135:189]
    local_binary_patterns = arr[189:203]
    haralick = arr[203:255]
    image = arr[255]

    newCell = Cell(image, area, bound, centroid, convex_hull_area, eccentricity, equivalent_diameter, euler_number,
                   extent,
                   inertia, intensity, label, major_axis, minor_axis, moments, orientation, perimeter, shannon_entropy,
                   solidity, moments_zernike, threshold_adjacency_statistics, local_binary_patterns, haralick)

    csvloc = str(id).rindex(".csv")
    filenamestr = str(id)[:csvloc+4]
    rowstr = str(id)[csvloc+4:]

    query = "hypi: {id: \"" + str(id) + "\"},\n"
    query += "image: \"" + str(image) + "\",\n"
    query += "filename: \"" + filenamestr + "\",\n"
    query += "row: " + rowstr + ",\n"
    query += "outlier: \"kmeans\",\n" 
    query += "area: " + str(int(area)) + ",\n"
    query += """bound: {
                    area: """ + str(bound[0]) + """,
                    max_column: """ + str(bound[1]) + """,
                    max_row: """ + str(bound[2]) + """,
                    min_column: """ + str(bound[3]) + """,
                    min_row: """ + str(bound[4]) + """
                    },\n"""
    query += """centroid: {
                    column: """ + str(centroid[0]) + """,
                    row: """ + str(centroid[1]) + """,
                    weighted_column: """ + str(centroid[2]) + """,
                    weighted_local_column: """ + str(centroid[3]) + """,
                    weighted_row: """ + str(centroid[4]) + """,
                    weighted_local_row: """ + str(centroid[5]) + """
                    },\n"""
    query += "convex_hull_area: " + str(int(convex_hull_area)) + ",\n"
    query += "eccentricity: " + str(eccentricity) + ",\n"
    query += "equivalent_diameter: " + str(equivalent_diameter) + ",\n"
    query += "euler_number: " + str(int(euler_number)) + ",\n"
    query += "extent: " + str(extent) + ",\n"
    query += """inertia: {
                    tensor_0_0: """ + str(inertia[0]) + """,
                    tensor_0_1: """ + str(inertia[1]) + """,
                    tensor_1_0: """ + str(inertia[2]) + """,
                    tensor_1_1: """ + str(inertia[3]) + """,
                    tensor_eigenvalues_0: """ + str(inertia[4]) + """,
                    tensor_eigenvalues_1: """ + str(inertia[5]) + """
                    },\n"""
    query += """intensity: {
                    integrated: """ + str(int(intensity[0])) + """,
                    maximum: """ + str(int(intensity[1])) + """,
                    mean: """ + str(intensity[2]) + """,
                    median: """ + str(int(intensity[3])) + """,
                    median_absolute_deviation: """ + str(int(intensity[4])) + """,
                    minimum: """ + str(int(intensity[5])) + """
                    quartile_1: """ + str(int(intensity[6])) + """,
                    quartile_2: """ + str(int(intensity[7])) + """,
                    quartile_3: """ + str(int(intensity[8])) + """,
                    standard_deviation: """ + str(intensity[9]) + """
                    },\n"""
    query += "label: " + str(int(label)) + ",\n"
    query += "major_axis: " + str(major_axis) + ",\n"
    query += "minor_axis: " + str(minor_axis) + ",\n"
    query += """moments: {
                    central: { 
                        _0_0: """ + str(moments[0]) + """,
                        _0_1: """ + str(moments[1]) + """,
                        _0_2: """ + str(moments[2]) + """,
                        _1_0: """ + str(moments[3]) + """,
                        _1_1: """ + str(moments[4]) + """,
                        _1_2: """ + str(moments[5]) + """,
                        _2_0: """ + str(moments[6]) + """,
                        _2_1: """ + str(moments[7]) + """,
                        _2_2: """ + str(moments[8]) + """
                        },
                    hu: {
                        _0: """ + str(moments[9]) + """,
                        _1: """ + str(moments[10]) + """,
                        _2: """ + str(moments[11]) + """,
                        _3: """ + str(moments[12]) + """,
                        _4: """ + str(moments[13]) + """,
                        _5: """ + str(moments[14]) + """,
                        _6: """ + str(moments[15]) + """
                        },
                    hu_weighted: {
                        _0: """ + str(moments[16]) + """,
                        _1: """ + str(moments[17]) + """,
                        _2: """ + str(moments[18]) + """,
                        _3: """ + str(moments[19]) + """,
                        _4: """ + str(moments[20]) + """,
                        _5: """ + str(moments[21]) + """,
                        _6: """ + str(moments[22]) + """
                        },              
                    normalized: {
                        _0_0: """ + str(moments[23]) + """,
                        _0_1: """ + str(moments[24]) + """,
                        _0_2: """ + str(moments[25]) + """,
                        _1_0: """ + str(moments[26]) + """,
                        _1_1: """ + str(moments[27]) + """,
                        _1_2: """ + str(moments[28]) + """,
                        _2_0: """ + str(moments[29]) + """,
                        _2_1: """ + str(moments[30]) + """,
                        _2_2: """ + str(moments[31]) + """
                        },
                    spatial: {
                        _0_0: """ + str(int(moments[32])) + """,
                        _0_1: """ + str(int(moments[33])) + """,
                        _0_2: """ + str(int(moments[34])) + """,
                        _1_0: """ + str(int(moments[35])) + """,
                        _1_1: """ + str(int(moments[36])) + """,
                        _1_2: """ + str(int(moments[37])) + """,
                        _2_0: """ + str(int(moments[38])) + """,
                        _2_1: """ + str(int(moments[39])) + """,
                        _2_2: """ + str(int(moments[40])) + """
                        },
                    weighted_central: {
                        _0_0: """ + str(moments[41]) + """,
                        _0_1: """ + str(moments[42]) + """,
                        _0_2: """ + str(moments[43]) + """,
                        _1_0: """ + str(moments[44]) + """,
                        _1_1: """ + str(moments[45]) + """,
                        _1_2: """ + str(moments[46]) + """,
                        _2_0: """ + str(moments[47]) + """,
                        _2_1: """ + str(moments[48]) + """,
                        _2_2: """ + str(moments[49]) + """
                        },
                    weighted_normalized: {
                        _0_0: """ + str(moments[50]) + """,
                        _0_1: """ + str(moments[51]) + """,
                        _0_2: """ + str(moments[52]) + """,
                        _1_0: """ + str(moments[53]) + """,
                        _1_1: """ + str(moments[54]) + """,
                        _1_2: """ + str(moments[55]) + """,
                        _2_0: """ + str(moments[56]) + """,
                        _2_1: """ + str(moments[57]) + """,
                        _2_2: """ + str(moments[58]) + """
                        },
                    weighted_spatial: {
                        _0_0: """ + str(int(moments[59])) + """,
                        _0_1: """ + str(int(moments[60])) + """,
                        _0_2: """ + str(int(moments[61])) + """,
                        _1_0: """ + str(int(moments[62])) + """,
                        _1_1: """ + str(int(moments[63])) + """,
                        _1_2: """ + str(int(moments[64])) + """,
                        _2_0: """ + str(int(moments[65])) + """,
                        _2_1: """ + str(int(moments[66])) + """,
                        _2_2: """ + str(int(moments[67])) + """
                        }
                    },\n"""
    query += "orientation: " + str(orientation) + ",\n"
    query += "perimeter: " + str(perimeter) + ",\n"
    query += """shannon_entropy: {
                    hartley: """ + str(shannon_entropy[0]) + """,
                    natural: """ + str(shannon_entropy[1]) + """,
                    shannon: """ + str(shannon_entropy[2]) + """
                    },\n"""
    query += "solidity: " + str(solidity) + ",\n"
    query += """moments_zernike: {
                    _0: """ + str(moments_zernike[0]) + """,
                    _1: """ + str(moments_zernike[1]) + """,
                    _2: """ + str(moments_zernike[2]) + """,
                    _3: """ + str(moments_zernike[3]) + """,
                    _4: """ + str(moments_zernike[4]) + """,
                    _5: """ + str(moments_zernike[5]) + """,
                    _6: """ + str(moments_zernike[6]) + """,
                    _7: """ + str(moments_zernike[7]) + """,
                    _8: """ + str(moments_zernike[8]) + """,
                    _9: """ + str(moments_zernike[9]) + """,
                    _10: """ + str(moments_zernike[10]) + """,
                    _11: """ + str(moments_zernike[11]) + """,
                    _12: """ + str(moments_zernike[12]) + """,
                    _13: """ + str(moments_zernike[13]) + """,
                    _14: """ + str(moments_zernike[14]) + """,
                    _15: """ + str(moments_zernike[15]) + """,
                    _16: """ + str(moments_zernike[16]) + """,
                    _17: """ + str(moments_zernike[17]) + """,
                    _18: """ + str(moments_zernike[18]) + """,
                    _19: """ + str(moments_zernike[19]) + """,
                    _20: """ + str(moments_zernike[20]) + """,
                    _21: """ + str(moments_zernike[21]) + """,
                    _22: """ + str(moments_zernike[22]) + """,
                    _23: """ + str(moments_zernike[23]) + """,
                    _24: """ + str(moments_zernike[24]) + """
                    },\n"""
    query += """threshold_adjacency_statistics: {
                        _0: """ + str(threshold_adjacency_statistics[0]) + """,
                        _1: """ + str(threshold_adjacency_statistics[1]) + """,
                        _2: """ + str(threshold_adjacency_statistics[2]) + """,
                        _3: """ + str(threshold_adjacency_statistics[3]) + """,
                        _4: """ + str(threshold_adjacency_statistics[4]) + """,
                        _5: """ + str(threshold_adjacency_statistics[5]) + """,
                        _6: """ + str(threshold_adjacency_statistics[6]) + """,
                        _7: """ + str(threshold_adjacency_statistics[7]) + """,
                        _8: """ + str(threshold_adjacency_statistics[8]) + """,
                        _9: """ + str(threshold_adjacency_statistics[9]) + """,
                        _10: """ + str(threshold_adjacency_statistics[10]) + """,
                        _11: """ + str(threshold_adjacency_statistics[11]) + """,
                        _12: """ + str(threshold_adjacency_statistics[12]) + """,
                        _13: """ + str(threshold_adjacency_statistics[13]) + """,
                        _14: """ + str(threshold_adjacency_statistics[14]) + """,
                        _15: """ + str(threshold_adjacency_statistics[15]) + """,
                        _16: """ + str(threshold_adjacency_statistics[16]) + """,
                        _17: """ + str(threshold_adjacency_statistics[17]) + """,
                        _18: """ + str(threshold_adjacency_statistics[18]) + """,
                        _19: """ + str(threshold_adjacency_statistics[19]) + """,
                        _20: """ + str(threshold_adjacency_statistics[20]) + """,
                        _21: """ + str(threshold_adjacency_statistics[21]) + """,
                        _22: """ + str(threshold_adjacency_statistics[22]) + """,
                        _23: """ + str(threshold_adjacency_statistics[23]) + """,
                        _24: """ + str(threshold_adjacency_statistics[24]) + """,
                        _25: """ + str(threshold_adjacency_statistics[25]) + """,
                        _26: """ + str(threshold_adjacency_statistics[26]) + """,
                        _27: """ + str(threshold_adjacency_statistics[27]) + """,
                        _28: """ + str(threshold_adjacency_statistics[28]) + """,
                        _29: """ + str(threshold_adjacency_statistics[29]) + """,
                        _30: """ + str(threshold_adjacency_statistics[30]) + """,
                        _31: """ + str(threshold_adjacency_statistics[31]) + """,
                        _32: """ + str(threshold_adjacency_statistics[32]) + """,
                        _33: """ + str(threshold_adjacency_statistics[33]) + """,
                        _34: """ + str(threshold_adjacency_statistics[34]) + """,
                        _35: """ + str(threshold_adjacency_statistics[35]) + """,
                        _36: """ + str(threshold_adjacency_statistics[36]) + """,
                        _37: """ + str(threshold_adjacency_statistics[37]) + """,
                        _38: """ + str(threshold_adjacency_statistics[38]) + """,
                        _39: """ + str(threshold_adjacency_statistics[39]) + """,
                        _40: """ + str(threshold_adjacency_statistics[40]) + """,
                        _41: """ + str(threshold_adjacency_statistics[41]) + """,
                        _42: """ + str(threshold_adjacency_statistics[42]) + """,
                        _43: """ + str(threshold_adjacency_statistics[43]) + """,
                        _44: """ + str(threshold_adjacency_statistics[44]) + """,
                        _45: """ + str(threshold_adjacency_statistics[45]) + """,
                        _46: """ + str(threshold_adjacency_statistics[46]) + """,
                        _47: """ + str(threshold_adjacency_statistics[47]) + """,
                        _48: """ + str(threshold_adjacency_statistics[48]) + """,
                        _49: """ + str(threshold_adjacency_statistics[49]) + """,
                        _50: """ + str(threshold_adjacency_statistics[50]) + """,
                        _51: """ + str(threshold_adjacency_statistics[51]) + """,
                        _52: """ + str(threshold_adjacency_statistics[52]) + """,
                        _53: """ + str(threshold_adjacency_statistics[53]) + """
                        },\n"""

    query += """local_binary_patterns: {
                        _0: """ + str(int(local_binary_patterns[0])) + """,
                        _1: """ + str(int(local_binary_patterns[1])) + """,
                        _2: """ + str(int(local_binary_patterns[2])) + """,
                        _3: """ + str(int(local_binary_patterns[3])) + """,
                        _4: """ + str(int(local_binary_patterns[4])) + """,
                        _5: """ + str(int(local_binary_patterns[5])) + """,
                        _6: """ + str(int(local_binary_patterns[6])) + """,
                        _7: """ + str(int(local_binary_patterns[7])) + """,
                        _8: """ + str(int(local_binary_patterns[8])) + """,
                        _9: """ + str(int(local_binary_patterns[9])) + """,
                        _10: """ + str(int(local_binary_patterns[10])) + """,
                        _11: """ + str(int(local_binary_patterns[11])) + """,
                        _12: """ + str(int(local_binary_patterns[12])) + """,
                        _13: """ + str(int(local_binary_patterns[13])) + """
                        },\n"""

    query += """haralick: {
                        _0: { 
                            angular_second_moment: """ + str(haralick[0]) + """,
                            contrast: """ + str(haralick[1]) + """,
                            correlation: """ + str(haralick[2]) + """,
                            ss_variance: """ + str(haralick[3]) + """,
                            inverse_difference_moment: """ + str(haralick[4]) + """,
                            sum_average: """ + str(haralick[5]) + """,
                            sum_variance: """ + str(haralick[6]) + """,
                            sum_entropy: """ + str(haralick[7]) + """,
                            entropy: """ + str(haralick[8]) + """,
                            difference_variance: """ + str(haralick[9]) + """,
                            difference_entropy: """ + str(haralick[10]) + """,
                            information_measure_of_correlation_1: """ + str(haralick[11]) + """,
                            information_measure_of_correlation_2: """ + str(haralick[12]) + """
                            },
                        _90: { 
                            angular_second_moment: """ + str(haralick[13]) + """,
                            contrast: """ + str(haralick[14]) + """,
                            correlation: """ + str(haralick[15]) + """,
                            ss_variance: """ + str(haralick[16]) + """,
                            inverse_difference_moment: """ + str(haralick[17]) + """,
                            sum_average: """ + str(haralick[18]) + """,
                            sum_variance: """ + str(haralick[19]) + """,
                            sum_entropy: """ + str(haralick[20]) + """,
                            entropy: """ + str(haralick[21]) + """,
                            difference_variance: """ + str(haralick[22]) + """,
                            difference_entropy: """ + str(haralick[23]) + """,
                            information_measure_of_correlation_1: """ + str(haralick[24]) + """,
                            information_measure_of_correlation_2: """ + str(haralick[25]) + """
                            },
                        _180: { 
                            angular_second_moment: """ + str(haralick[26]) + """,
                            contrast: """ + str(haralick[27]) + """,
                            correlation: """ + str(haralick[28]) + """,
                            ss_variance: """ + str(haralick[29]) + """,
                            inverse_difference_moment: """ + str(haralick[30]) + """,
                            sum_average: """ + str(haralick[31]) + """,
                            sum_variance: """ + str(haralick[32]) + """,
                            sum_entropy: """ + str(haralick[33]) + """,
                            entropy: """ + str(haralick[34]) + """,
                            difference_variance: """ + str(haralick[35]) + """,
                            difference_entropy: """ + str(haralick[36]) + """,
                            information_measure_of_correlation_1: """ + str(haralick[37]) + """,
                            information_measure_of_correlation_2: """ + str(haralick[38]) + """
                            },
                        _270: { 
                            angular_second_moment: """ + str(haralick[39]) + """,
                            contrast: """ + str(haralick[40]) + """,
                            correlation: """ + str(haralick[41]) + """,
                            ss_variance: """ + str(haralick[42]) + """,
                            inverse_difference_moment: """ + str(haralick[43]) + """,
                            sum_average: """ + str(haralick[44]) + """,
                            sum_variance: """ + str(haralick[45]) + """,
                            sum_entropy: """ + str(haralick[46]) + """,
                            entropy: """ + str(haralick[47]) + """,
                            difference_variance: """ + str(haralick[48]) + """,
                            difference_entropy: """ + str(haralick[49]) + """,
                            information_measure_of_correlation_1: """ + str(haralick[50]) + """,
                            information_measure_of_correlation_2: """ + str(haralick[51]) + """
                            }
                        }\n"""

    querysplit = query.splitlines()
    query2 = ""
    toCheck = ":  ,"
    for i in range(len(querysplit)):
        if toCheck in querysplit[i]:
            pass
        else:
            query2 += querysplit[i] + "\n"

    # print(rowstr) #printing test
    return query2


#print(retrievecells("features.csv"))
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
import sys
pd.options.mode.chained_assignment = None  # default='warn'

# filename = sys.argv[1]

# filename = "features.csv"

skopy_data = 'C:/Users/paulk/PycharmProjects/vertex-main/vertex-main/shkim219/data/features.csv'

headers = {'Authorization': 'eyJhbGciOiJSUzI1NiJ9.eyJoeXBpLmxvZ2luIjp0cnVlLCJoeXBpLnVzZXJuYW1lIjoic2hraW0yMTlAYnUuZWR1IiwiaHlwaS5lbWFpbCI6InNoa2ltMjE5QGJ1LmVkdSIsImF1ZCI6IjAxRjdWNDE3MFpERFNFWUY4OFZaVDVaNEdGIiwiaWF0IjoxNjI4Njk0OTE2LCJleHAiOjE2MzEyODY5MTYsInN1YiI6IjAxRjdWNDE3MFo0R0NDWllSNVcyTTBKUTA0IiwibmJmIjoxNjI4Njk0OTE2fQ.rELYlvjIMk9MX8POZ8ARy-5jTtUEHrSLa8UGbbmIVWRunNYq4_Eb5ClaBIPCvEcnOCI0x75pT9SfGHyvDwR4Z5FmKj4oRn-M2qe0-nC2W7trx9px1oDobHT8S1j63NvQqD85ZKLj2QqOE1WOOsC8JKprja0GKIlLcwX2LaL_7WSG5eQ52BP9R2MFrPEqeaUjilZQau7FPkwLeQ1hfPds_iPLmY4cBfYaBFAS_bPyZ5a05OlD_UyQFQI5GsHaL8fWsA77icaRo2_MKB5ynQRpvBEB133cupFVlzP-QwyOdCmeJoo6dGiPyN-7C_7w8KntTSH5U1Y0bRGnd421psXZaw',
           'hypi-domain': 'clamming.apps.hypi.app'}

transport = AIOHTTPTransport(url='https://api.hypi.app/graphql', headers=headers)
client = Client(transport=transport, fetch_schema_from_transport=True)


class Cell:
    def __init__(self, classification, image, area, bound, centroid, convex_hull_area, eccentricity, equivalent_diameter, euler_number,
                 extent,
                 inertia, intensity, label, major_axis, minor_axis, moments, orientation, perimeter, shannon_entropy,
                 solidity, moments_zernike, threshold_adjacency_statistics, local_binary_patterns, haralick):
        self.classification = classification
        self.image = image
        self.area = area
        self.bound = bound
        self.centroid = centroid
        self.convex_hull_area = convex_hull_area
        self.eccentricity = eccentricity
        self.equivalent_diameter = equivalent_diameter
        self.euler_number = euler_number
        self.extent = extent
        self.inertia = inertia
        self.intensity = intensity
        self.label = label
        self.major_axis = major_axis
        self.minor_axis = minor_axis
        self.moments = moments
        self.orientation = orientation
        self.perimeter = perimeter
        self.shannon_entropy = shannon_entropy
        self.solidity = solidity
        self.moments_zernike = moments_zernike
        self.threshold_adjacency_statistics = threshold_adjacency_statistics
        self.local_binary_patterns = local_binary_patterns
        self.haralick = haralick


def one_cell(arr, id):
    for i in range(len(arr)):
        if str(arr[i]) == 'nan':
            arr[i] = " "
    # print(len(arr))
    classification = arr[0]
    area = arr[1]
    bound = arr[2:7]
    centroid = arr[7:13]
    convex_hull_area = arr[13]
    eccentricity = arr[14]
    equivalent_diameter = arr[15]
    euler_number = arr[16]
    extent = arr[17]
    inertia = arr[18:24]
    intensity = arr[24:34]
    label = arr[34]
    major_axis = arr[35]
    minor_axis = arr[36]
    moments = arr[37:105]
    orientation = arr[105]
    perimeter = arr[106]
    shannon_entropy = arr[107:110]
    solidity = arr[110]
    moments_zernike = arr[111:136]
    threshold_adjacency_statistics = arr[136:190]
    local_binary_patterns = arr[190:204]
    haralick = arr[204:256]
    image = arr[256]

    newCell = Cell(classification, image, area, bound, centroid, convex_hull_area, eccentricity, equivalent_diameter, euler_number,
                   extent,
                   inertia, intensity, label, major_axis, minor_axis, moments, orientation, perimeter, shannon_entropy,
                   solidity, moments_zernike, threshold_adjacency_statistics, local_binary_patterns, haralick)

    csvloc = str(id).rindex(".csv")
    filenamestr = str(id)[:csvloc+4]
    rowstr = str(id)[csvloc+4:]

    query = "hypi: {id: \"" + str(id) + "\"},\n"
    queryFirst = "image: \"" + str(image) + "\",\n"
    queryFirst += "filename: \"" + filenamestr + "\",\n"
    queryFirst += "row: " + rowstr + ",\n"
    queryFirst += "classification: " + str(int(classification)) + ",\n"
    queryFirst += "area: " + str(int(area)) + ",\n"
    querySecond = """bound: {
                    area: """ + str(bound[0]) + """,
                    max_column: """ + str(bound[1]) + """,
                    max_row: """ + str(bound[2]) + """,
                    min_column: """ + str(bound[3]) + """,
                    min_row: """ + str(bound[4]) + """
                    },\n"""
    queryThird = """centroid: {
                    column: """ + str(centroid[0]) + """,
                    row: """ + str(centroid[1]) + """,
                    weighted_column: """ + str(centroid[2]) + """,
                    weighted_local_column: """ + str(centroid[3]) + """,
                    weighted_row: """ + str(centroid[4]) + """,
                    weighted_local_row: """ + str(centroid[5]) + """
                    },\n"""
    queryFourth = "convex_hull_area: " + str(int(convex_hull_area)) + ",\n"
    queryFourth += "eccentricity: " + str(eccentricity) + ",\n"
    queryFourth += "equivalent_diameter: " + str(equivalent_diameter) + ",\n"
    queryFourth += "euler_number: " + str(int(euler_number)) + ",\n"
    queryFourth += "extent: " + str(extent) + ",\n"
    queryFifth = """inertia: {
                    tensor_0_0: """ + str(inertia[0]) + """,
                    tensor_0_1: """ + str(inertia[1]) + """,
                    tensor_1_0: """ + str(inertia[2]) + """,
                    tensor_1_1: """ + str(inertia[3]) + """,
                    tensor_eigenvalues_0: """ + str(inertia[4]) + """,
                    tensor_eigenvalues_1: """ + str(inertia[5]) + """
                    },\n"""
    querySixth = """intensity: {
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
    querySeventh = "label: " + str(int(label)) + ",\n"
    querySeventh += "major_axis: " + str(major_axis) + ",\n"
    querySeventh += "minor_axis: " + str(minor_axis) + ",\n"
    queryEighth = """moments: {
                    central: { 
                        _0_0: """ + str(moments[0]) + """,
                        _0_1: """ + str(moments[1]) + """,
                        _0_2: """ + str(moments[2]) + """,
                        _1_0: """ + str(moments[3]) + """,
                                            },
                      },\n"""  
    queryEighth0 = """moments: {
                    central: { 
                        _1_1: """ + str(moments[4]) + """,
                        _1_2: """ + str(moments[5]) + """,
                        _2_0: """ + str(moments[6]) + """,
                        _2_1: """ + str(moments[7]) + """,
                        _2_2: """ + str(moments[8]) + """
                        },
                      },\n"""             
    queryEighth1 = """moments: {
                        hu: {
                        _0: """ + str(moments[9]) + """,
                        _1: """ + str(moments[10]) + """,
                        _2: """ + str(moments[11]) + """,
                        _3: """ + str(moments[12]) + """,
                        _4: """ + str(moments[13]) + """,
                        _5: """ + str(moments[14]) + """,
                        _6: """ + str(moments[15]) + """
                        },
                      },\n"""   
    queryEighth2 = """moments: {
                    hu_weighted: {
                        _0: """ + str(moments[16]) + """,
                        _1: """ + str(moments[17]) + """,
                        _2: """ + str(moments[18]) + """,
                        _3: """ + str(moments[19]) + """,
                        _4: """ + str(moments[20]) + """,
                        _5: """ + str(moments[21]) + """,
                        _6: """ + str(moments[22]) + """
                        },
                      },\n"""  
    queryEighth3 = """moments: {               
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
                      },\n"""   
    queryEighth4 = """moments: {
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
                      },\n"""   
    queryEighth5 = """moments: {
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
                      },\n"""
    queryEighth6 = """moments: {   
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
                      },\n"""  
    queryEighth7 = """moments: { 
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
    queryNinth = "orientation: " + str(orientation) + ",\n"
    queryNinth += "perimeter: " + str(perimeter) + ",\n"
    queryNinth1 = """shannon_entropy: {
                    hartley: """ + str(shannon_entropy[0]) + """,
                    natural: """ + str(shannon_entropy[1]) + """,
                    shannon: """ + str(shannon_entropy[2]) + """
                    },\n"""
    queryNinth1 += "solidity: " + str(solidity) + ",\n"
    queryTenth = """moments_zernike: {
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
                    },\n"""
    queryTenth1 = """moments_zernike: {            
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
    queryEleventh = """threshold_adjacency_statistics: {
                        _0: """ + str(threshold_adjacency_statistics[0]) + """,
                        _1: """ + str(threshold_adjacency_statistics[1]) + """,
                        _2: """ + str(threshold_adjacency_statistics[2]) + """,
                        _3: """ + str(threshold_adjacency_statistics[3]) + """,
                        _4: """ + str(threshold_adjacency_statistics[4]) + """,
                        },\n"""
    queryEleventh0 =  """threshold_adjacency_statistics: {
                        _5: """ + str(threshold_adjacency_statistics[5]) + """,
                        _6: """ + str(threshold_adjacency_statistics[6]) + """,
                        _7: """ + str(threshold_adjacency_statistics[7]) + """,
                        _8: """ + str(threshold_adjacency_statistics[8]) + """,
                        _9: """ + str(threshold_adjacency_statistics[9]) + """,
                        _10: """ + str(threshold_adjacency_statistics[10]) + """,
                        },\n"""
    queryEleventh1 = """threshold_adjacency_statistics: {
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
                        },\n"""
    queryEleventh2 = """threshold_adjacency_statistics: {
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
                        },\n"""
    queryEleventh3 = """threshold_adjacency_statistics: {
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
                        },\n"""
    queryEleventh4 = """threshold_adjacency_statistics: {
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
                        },\n"""
    queryEleventh5 = """threshold_adjacency_statistics: {
                        _51: """ + str(threshold_adjacency_statistics[51]) + """,
                        _52: """ + str(threshold_adjacency_statistics[52]) + """,
                        _53: """ + str(threshold_adjacency_statistics[53]) + """
                        },\n"""

    queryTwelvth = """local_binary_patterns: {
                        _0: """ + str(int(local_binary_patterns[0])) + """,
                        _1: """ + str(int(local_binary_patterns[1])) + """,
                        _2: """ + str(int(local_binary_patterns[2])) + """,
                        _3: """ + str(int(local_binary_patterns[3])) + """,
                        _4: """ + str(int(local_binary_patterns[4])) + """,
                        _5: """ + str(int(local_binary_patterns[5])) + """,
                        },\n"""
    queryTwelvth0 = """local_binary_patterns: {
                        _6: """ + str(int(local_binary_patterns[6])) + """,
                        _7: """ + str(int(local_binary_patterns[7])) + """,
                        _8: """ + str(int(local_binary_patterns[8])) + """,
                        _9: """ + str(int(local_binary_patterns[9])) + """,
                        _10: """ + str(int(local_binary_patterns[10])) + """,
                        _11: """ + str(int(local_binary_patterns[11])) + """,
                        _12: """ + str(int(local_binary_patterns[12])) + """,
                        _13: """ + str(int(local_binary_patterns[13])) + """
                        },\n"""

    queryThirteenth = """haralick: {
                        _0: { 
                            angular_second_moment: """ + str(haralick[0]) + """,
                            contrast: """ + str(haralick[1]) + """,
                            correlation: """ + str(haralick[2]) + """,
                            ss_variance: """ + str(haralick[3]) + """,
                            inverse_difference_moment: """ + str(haralick[4]) + """,
                            sum_average: """ + str(haralick[5]) + """,
                            sum_variance: """ + str(haralick[6]) + """,
                                                        },
                        }\n"""
    queryThirteenth0 = """haralick: {
                        _0: { 
                            sum_entropy: """ + str(haralick[7]) + """,
                            entropy: """ + str(haralick[8]) + """,
                            difference_variance: """ + str(haralick[9]) + """,
                            difference_entropy: """ + str(haralick[10]) + """,
                            information_measure_of_correlation_1: """ + str(haralick[11]) + """,
                            information_measure_of_correlation_2: """ + str(haralick[12]) + """
                            },
                        }\n"""
    queryThirteenth1 = """haralick: {
                        _90: { 
                            angular_second_moment: """ + str(haralick[13]) + """,
                            contrast: """ + str(haralick[14]) + """,
                            correlation: """ + str(haralick[15]) + """,
                            ss_variance: """ + str(haralick[16]) + """,
                                                                                    },
                        }\n"""
    queryThirteenth10 = """haralick: {
                        _90: { 
                            inverse_difference_moment: """ + str(haralick[17]) + """,
                            sum_average: """ + str(haralick[18]) + """,
                            sum_variance: """ + str(haralick[19]) + """,
                                                        },
                        }\n"""
    
    queryThirteenth11 = """haralick: {
                        _90: { 
                            sum_entropy: """ + str(haralick[20]) + """,
                            entropy: """ + str(haralick[21]) + """,
                            difference_variance: """ + str(haralick[22]) + """,
                            difference_entropy: """ + str(haralick[23]) + """,
                            information_measure_of_correlation_1: """ + str(haralick[24]) + """,
                            information_measure_of_correlation_2: """ + str(haralick[25]) + """
                            },
                        }\n"""
    queryThirteenth2 = """haralick: {
                        _180: { 
                            angular_second_moment: """ + str(haralick[26]) + """,
                            contrast: """ + str(haralick[27]) + """,
                            correlation: """ + str(haralick[28]) + """,
                            ss_variance: """ + str(haralick[29]) + """,
                            inverse_difference_moment: """ + str(haralick[30]) + """,
                            sum_average: """ + str(haralick[31]) + """,
                            sum_variance: """ + str(haralick[32]) + """,
                                                      },
                        }\n"""
    queryThirteenth20 = """haralick: {
                        _180: { 
                            sum_entropy: """ + str(haralick[33]) + """,
                            entropy: """ + str(haralick[34]) + """,
                            difference_variance: """ + str(haralick[35]) + """,
                            difference_entropy: """ + str(haralick[36]) + """,
                            information_measure_of_correlation_1: """ + str(haralick[37]) + """,
                            information_measure_of_correlation_2: """ + str(haralick[38]) + """
                            },
                        }\n"""
    queryThirteenth3 = """haralick: {
                        _270: { 
                            angular_second_moment: """ + str(haralick[39]) + """,
                            contrast: """ + str(haralick[40]) + """,
                            correlation: """ + str(haralick[41]) + """,
                            ss_variance: """ + str(haralick[42]) + """,
                            inverse_difference_moment: """ + str(haralick[43]) + """,
                            sum_average: """ + str(haralick[44]) + """,
                            sum_variance: """ + str(haralick[45]) + """,
                                                        },
                        }\n"""
    queryThirteenth30 = """haralick: {
                        _270: { 
                            sum_entropy: """ + str(haralick[46]) + """,
                            entropy: """ + str(haralick[47]) + """,
                            difference_variance: """ + str(haralick[48]) + """,
                            difference_entropy: """ + str(haralick[49]) + """,
                            information_measure_of_correlation_1: """ + str(haralick[50]) + """,
                            information_measure_of_correlation_2: """ + str(haralick[51]) + """
                            }
                        }\n"""

    returnQuery = [queryFirst, querySecond, queryThird, queryFourth, queryFifth, 
    querySixth, querySeventh, queryEighth, queryEighth0, queryEighth1, queryEighth2, queryEighth3, queryEighth4,
    queryEighth5, queryEighth6, queryEighth7, queryNinth, queryNinth1, queryTenth, queryTenth1, queryEleventh, 
     queryEleventh0, queryEleventh1, queryEleventh2, queryEleventh3, queryEleventh4, queryEleventh5, queryTwelvth,
     queryTwelvth0, queryThirteenth, queryThirteenth0, queryThirteenth1, queryThirteenth10, 
     queryThirteenth11, queryThirteenth2, queryThirteenth20, queryThirteenth3,queryThirteenth30]

    returnQueryChecked = []

    toCheck = ":  ,"

    for i in range(len(returnQuery)):
      querysplit = returnQuery[i].splitlines()
      queryCheck = ""
      for i in range(len(querysplit)):
          if toCheck in querysplit[i]:
              pass
          else:
              queryCheck += querysplit[i] + "\n"
      returnQueryChecked.append(queryCheck)

    # print(rowstr) #printing test
    return returnQueryChecked



def one_cell_original(arr, id):
    for i in range(len(arr)):
        if str(arr[i]) == 'nan':
            arr[i] = " "
    # print(len(arr))
    classification = arr[0]
    area = arr[1]
    bound = arr[2:7]
    centroid = arr[7:13]
    convex_hull_area = arr[13]
    eccentricity = arr[14]
    equivalent_diameter = arr[15]
    euler_number = arr[16]
    extent = arr[17]
    inertia = arr[18:24]
    intensity = arr[24:34]
    label = arr[34]
    major_axis = arr[35]
    minor_axis = arr[36]
    moments = arr[37:105]
    orientation = arr[105]
    perimeter = arr[106]
    shannon_entropy = arr[107:110]
    solidity = arr[110]
    moments_zernike = arr[111:136]
    threshold_adjacency_statistics = arr[136:190]
    local_binary_patterns = arr[190:204]
    haralick = arr[204:256]
    image = arr[256]

    newCell = Cell(image, classification, area, bound, centroid, convex_hull_area, eccentricity, equivalent_diameter, euler_number,
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
    query += "classification: " + str(int(classification)) + ",\n"
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



    toCheck = ":  ,"
    querysplit = query.splitlines()
    queryCheck = ""
    for i in range(len(querysplit)):
        if toCheck in querysplit[i]:
            pass
        else:
            queryCheck += querysplit[i] + "\n"

    # print(rowstr) #printing test
    return queryCheck








def create_cell(file):
    df = pd.read_csv(file)
    df.dropna(how="all", inplace=True)
    for i in range(len(df)):
        createcell((i+1), df.iloc[i], file)

def create_cell_original(file):
  df = pd.read_csv(file)
  df.dropna(how="all", inplace=True)
  for i in range(len(df)):
      createcell_original((i+1), df.iloc[i], file)

def getFiles():
    query = gql(
        """
        {
            find(type: Filename, arcql: "* SORT hypi.id ASC"){
                edges {
                    node {
                        ... on Filename {
                            csvname
                            totalnumber
                        }
                    }
                }
            }
        }
        """
    )

    return client.execute(query)
  

def findtest(filename):
    query = gql(
        """
        {
          find(type: Cell, arcql: "filename = \'""" + filename + """\' SORT row ASC") {
            edges {
              node {
                ... on Cell {
                  hypi {
                    id
                  }
                  image
                }
            }
        }
    }
    }
    """
    )
    return client.execute(query)


def find(filename):
    query = gql(
        """
            {
              find(type: Cell, arcql: "filename = \'""" + filename + """\' SORT row ASC") {
                edges {
                  node {
                    ... on Cell {
                      hypi {
                        id
                      }
                      image
                      classification
                      area
                      bound {
                        area
                        max_column
                        max_row
                        min_column
                        min_row
                      }   
                      centroid {
                      column
                      row
                        weighted_column
                        weighted_local_column
                        weighted_row
                        weighted_local_row
                      }
                      convex_hull_area
                      eccentricity
                      equivalent_diameter
                      euler_number
                      extent
                      inertia {
                          tensor_0_0
                        tensor_0_1
                        tensor_1_0
                        tensor_1_1
                        tensor_eigenvalues_0
                        tensor_eigenvalues_1
                      }
                      intensity {
                          integrated
                            maximum
                            mean
                            median
                            median_absolute_deviation
                            minimum
                            quartile_1
                            quartile_2
                            quartile_3
                            standard_deviation
                      }
                      label
                      major_axis
                      minor_axis
                      moments {
                          central {
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            hu {
                                _0
                                _1
                                _2
                                _3
                                _4
                                _5
                                _6
                          }
                            hu_weighted{
                                _0
                                _1
                                _2
                                _3
                                _4
                                _5
                                _6
                          }
                            normalized{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            spatial{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            weighted_central{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            weighted_normalized{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            weighted_spatial{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                      }
                      orientation
                      perimeter
                      shannon_entropy {
                        hartley
                        natural
                        shannon                 
                      }
                      solidity
                      moments_zernike {
                            _0
                            _1
                            _2
                            _3
                            _4
                            _5
                            _6
                            _7
                            _8
                            _9
                            _10
                            _11
                            _12
                            _13
                            _14
                            _15
                            _16
                            _17
                            _18
                            _19
                            _20
                            _21
                            _22
                            _23
                            _24
                      }
                      threshold_adjacency_statistics {
                            _0
                            _1
                            _2
                            _3
                            _4
                            _5
                            _6
                            _7
                            _8
                            _9
                            _10
                            _11
                            _12
                            _13
                            _14
                            _15
                            _16
                            _17
                            _18
                            _19
                            _20
                            _21
                            _22
                            _23
                            _24
                            _25
                            _26
                            _27
                            _28
                            _29
                            _30
                            _31
                            _32
                            _33
                            _34
                            _35
                            _36
                            _37
                            _38
                            _39
                            _40
                            _41
                            _42
                            _43
                            _44
                            _45
                            _46
                            _47
                            _48
                            _49
                            _50
                            _51
                            _52
                            _53
                      }
                      local_binary_patterns  {
                            _0
                            _1
                            _2
                            _3
                            _4
                            _5
                            _6
                            _7
                            _8
                            _9
                            _10
                            _11
                            _12
                            _13
                      }
                      haralick {
                        _0 {
                            angular_second_moment
                            contrast
                            correlation
                            ss_variance
                            inverse_difference_moment
                            sum_average
                            sum_variance
                            sum_entropy
                            entropy
                            difference_variance
                            difference_entropy
                            information_measure_of_correlation_1
                            information_measure_of_correlation_2
                        }
                        _90 {
                            angular_second_moment
                            contrast
                            correlation
                            ss_variance
                            inverse_difference_moment
                            sum_average
                            sum_variance
                            sum_entropy
                            entropy
                            difference_variance
                            difference_entropy
                            information_measure_of_correlation_1
                            information_measure_of_correlation_2
                        }
                        _180 {
                            angular_second_moment
                            contrast
                            correlation
                            ss_variance
                            inverse_difference_moment
                            sum_average
                            sum_variance
                            sum_entropy
                            entropy
                            difference_variance
                            difference_entropy
                            information_measure_of_correlation_1
                            information_measure_of_correlation_2
                        }
                        _270 {
                            angular_second_moment
                            contrast
                            correlation
                            ss_variance
                            inverse_difference_moment
                            sum_average
                            sum_variance
                            sum_entropy
                            entropy
                            difference_variance
                            difference_entropy
                            information_measure_of_correlation_1
                            information_measure_of_correlation_2
                        }
                      }
                    }
                  }
                  cursor
                }
              }
            }
        """
        )


    return client.execute(query)


def findcells(filename, no, current):
    query = gql(
        """
            {
              find(type: Cell, arcql: "filename = \'""" + filename + """\' AND row IN [ """ + str(current) + ", " + str(current+no) + """) SORT row ASC") {
                edges {
                  node {
                    ... on Cell {
                      image
                      classification
                      area
                      bound {
                        area
                        max_column
                        max_row
                        min_column
                        min_row
                      }   
                      centroid {
                      column
                      row
                        weighted_column
                        weighted_local_column
                        weighted_row
                        weighted_local_row
                      }
                      convex_hull_area
                      eccentricity
                      equivalent_diameter
                      euler_number
                      extent
                      inertia {
                          tensor_0_0
                        tensor_0_1
                        tensor_1_0
                        tensor_1_1
                        tensor_eigenvalues_0
                        tensor_eigenvalues_1
                      }
                      intensity {
                          integrated
                            maximum
                            mean
                            median
                            median_absolute_deviation
                            minimum
                            quartile_1
                            quartile_2
                            quartile_3
                            standard_deviation
                      }
                      label
                      major_axis
                      minor_axis
                      moments {
                          central {
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            hu {
                                _0
                                _1
                                _2
                                _3
                                _4
                                _5
                                _6
                          }
                            hu_weighted{
                                _0
                                _1
                                _2
                                _3
                                _4
                                _5
                                _6
                          }
                            normalized{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            spatial{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            weighted_central{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            weighted_normalized{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                            weighted_spatial{
                              _0_0
                                _0_1
                                _0_2
                                _1_0
                                _1_1
                                _1_2
                                _2_0
                                _2_1
                                _2_2
                          }
                      }
                      orientation
                      perimeter
                      shannon_entropy {
                        hartley
                        natural
                        shannon                 
                      }
                      solidity
                      moments_zernike {
                            _0
                            _1
                            _2
                            _3
                            _4
                            _5
                            _6
                            _7
                            _8
                            _9
                            _10
                            _11
                            _12
                            _13
                            _14
                            _15
                            _16
                            _17
                            _18
                            _19
                            _20
                            _21
                            _22
                            _23
                            _24
                      }
                      threshold_adjacency_statistics {
                            _0
                            _1
                            _2
                            _3
                            _4
                            _5
                            _6
                            _7
                            _8
                            _9
                            _10
                            _11
                            _12
                            _13
                            _14
                            _15
                            _16
                            _17
                            _18
                            _19
                            _20
                            _21
                            _22
                            _23
                            _24
                            _25
                            _26
                            _27
                            _28
                            _29
                            _30
                            _31
                            _32
                            _33
                            _34
                            _35
                            _36
                            _37
                            _38
                            _39
                            _40
                            _41
                            _42
                            _43
                            _44
                            _45
                            _46
                            _47
                            _48
                            _49
                            _50
                            _51
                            _52
                            _53
                      }
                      local_binary_patterns  {
                            _0
                            _1
                            _2
                            _3
                            _4
                            _5
                            _6
                            _7
                            _8
                            _9
                            _10
                            _11
                            _12
                            _13
                      }
                      haralick {
                        _0 {
                            angular_second_moment
                            contrast
                            correlation
                            ss_variance
                            inverse_difference_moment
                            sum_average
                            sum_variance
                            sum_entropy
                            entropy
                            difference_variance
                            difference_entropy
                            information_measure_of_correlation_1
                            information_measure_of_correlation_2
                        }
                        _90 {
                            angular_second_moment
                            contrast
                            correlation
                            ss_variance
                            inverse_difference_moment
                            sum_average
                            sum_variance
                            sum_entropy
                            entropy
                            difference_variance
                            difference_entropy
                            information_measure_of_correlation_1
                            information_measure_of_correlation_2
                        }
                        _180 {
                            angular_second_moment
                            contrast
                            correlation
                            ss_variance
                            inverse_difference_moment
                            sum_average
                            sum_variance
                            sum_entropy
                            entropy
                            difference_variance
                            difference_entropy
                            information_measure_of_correlation_1
                            information_measure_of_correlation_2
                        }
                        _270 {
                            angular_second_moment
                            contrast
                            correlation
                            ss_variance
                            inverse_difference_moment
                            sum_average
                            sum_variance
                            sum_entropy
                            entropy
                            difference_variance
                            difference_entropy
                            information_measure_of_correlation_1
                            information_measure_of_correlation_2
                        }
                      }
                    }
                  }
                }
              }
            }
        """
        )


    return client.execute(query)



def makecell(stringfromquery):
    cellDictionary = eval(stringfromquery)
    val = cellDictionary.values()
    keys = cellDictionary.keys()
    cellImage = [cellDictionary["image"]]

    cellClassification = [cellDictionary["classification"]]
    cellArea = [cellDictionary["area"]]

    cellBound = cellDictionary["bound"]
    cellBoundDictionary = eval(str(cellBound))
    cellBoundArea = cellBoundDictionary["area"]
    cellBoundMaxCol = cellBoundDictionary["max_column"]
    cellBoundMaxRow = cellBoundDictionary["max_row"]
    cellBoundMinCol = cellBoundDictionary["min_column"]
    cellBoundMinRow = cellBoundDictionary["min_row"]
    cellBoundArray = list(cellBoundDictionary.values())


    cellCentroid = cellDictionary["centroid"]
    cellCentroidDictionary = eval(str(cellCentroid))
    cellCentroidColumn = cellCentroidDictionary["column"]
    cellCentroidRow = cellCentroidDictionary["row"]
    cellCentroidWeightedColumn = cellCentroidDictionary["weighted_column"]
    cellCentroidWeightedLocalColumn = cellCentroidDictionary["weighted_local_column"]
    cellCentroidWeightedRow = cellCentroidDictionary["weighted_row"]
    cellCentroidWeightedLocalRow = cellCentroidDictionary["weighted_local_row"]
    cellCentroidArray = list(cellCentroidDictionary.values())

    cellConvex = [cellDictionary["convex_hull_area"]]

    cellEccentricity = [cellDictionary["eccentricity"]]

    cellDiameter = [cellDictionary["equivalent_diameter"]]

    cellEuler = [cellDictionary["euler_number"]]

    cellExtent = [cellDictionary["extent"]]

    cellInertia = cellDictionary["inertia"]
    cellInertiaDictionary = eval(str(cellInertia))
    cellInertiaTensor00 = cellInertiaDictionary["tensor_0_0"]
    cellInertiaTensor01 = cellInertiaDictionary["tensor_0_1"]
    cellInertiaTensor10 = cellInertiaDictionary["tensor_1_0"]
    cellInertiaTensor11 = cellInertiaDictionary["tensor_1_1"]
    cellInertiaTensorEigenvalues0 = cellInertiaDictionary["tensor_eigenvalues_0"]
    cellInertiaTensorEigenvalues1 = cellInertiaDictionary["tensor_eigenvalues_1"]
    cellInertiaArray = list(cellInertiaDictionary.values())

    cellIntensity = cellDictionary["intensity"]
    cellIntensityDictionary = eval(str(cellIntensity))
    cellIntensityIntegrated = cellIntensityDictionary["integrated"]
    cellIntensityMaximum = cellIntensityDictionary["maximum"]
    cellIntensityMean = cellIntensityDictionary["mean"]
    cellIntensityMedian = cellIntensityDictionary["median"]
    cellIntensityMedianAbsoluteDeviation = cellIntensityDictionary["median_absolute_deviation"]
    cellIntensityMinimum = cellIntensityDictionary["minimum"]
    cellIntensityQuartile1 = cellIntensityDictionary["quartile_1"]
    cellIntensityQuartile2 = cellIntensityDictionary["quartile_2"]
    cellIntensityQuartile3 = cellIntensityDictionary["quartile_3"]
    cellIntensityStandardDeviation = cellIntensityDictionary["standard_deviation"]
    cellIntensityArray = list(cellIntensityDictionary.values())

    cellLabel = [cellDictionary["label"]]

    cellMajor = [cellDictionary["major_axis"]]

    cellMinor = [cellDictionary["minor_axis"]]

    cellMoments = cellDictionary["moments"]
    cellMomentsDictionary = eval(str(cellMoments))

    cellMomentsCentral = cellMomentsDictionary["central"]
    cellMomentsCentralDictionary = eval(str(cellMomentsCentral))
    cellMomentsCentral00 = cellMomentsCentralDictionary["_0_0"]
    cellMomentsCentral01 = cellMomentsCentralDictionary["_0_1"]
    cellMomentsCentral02 = cellMomentsCentralDictionary["_0_2"]
    cellMomentsCentral10 = cellMomentsCentralDictionary["_1_0"]
    cellMomentsCentral11 = cellMomentsCentralDictionary["_1_1"]
    cellMomentsCentral12 = cellMomentsCentralDictionary["_1_2"]
    cellMomentsCentral20 = cellMomentsCentralDictionary["_2_0"]
    cellMomentsCentral21 = cellMomentsCentralDictionary["_2_1"]
    cellMomentsCentral22 = cellMomentsCentralDictionary["_2_2"]

    cellMomentsHu = cellMomentsDictionary["hu"]
    cellMomentsHuDictionary = eval(str(cellMomentsHu))
    cellMomentsHu0 = cellMomentsHuDictionary["_0"]
    cellMomentsHu1 = cellMomentsHuDictionary["_1"]
    cellMomentsHu2 = cellMomentsHuDictionary["_2"]
    cellMomentsHu3 = cellMomentsHuDictionary["_3"]
    cellMomentsHu4 = cellMomentsHuDictionary["_4"]
    cellMomentsHu5 = cellMomentsHuDictionary["_5"]
    cellMomentsHu6 = cellMomentsHuDictionary["_6"]

    cellMomentsHuWeighted = cellMomentsDictionary["hu_weighted"]
    cellMomentsHuWeightedDictionary = eval(str(cellMomentsHuWeighted))
    cellMomentsHuWeighted0 = cellMomentsHuWeightedDictionary["_0"]
    cellMomentsHuWeighted1 = cellMomentsHuWeightedDictionary["_1"]
    cellMomentsHuWeighted2 = cellMomentsHuWeightedDictionary["_2"]
    cellMomentsHuWeighted3 = cellMomentsHuWeightedDictionary["_3"]
    cellMomentsHuWeighted4 = cellMomentsHuWeightedDictionary["_4"]
    cellMomentsHuWeighted5 = cellMomentsHuWeightedDictionary["_5"]
    cellMomentsHuWeighted6 = cellMomentsHuWeightedDictionary["_6"]

    cellMomentsNormalized = cellMomentsDictionary["normalized"]
    cellMomentsNormalizedDictionary = eval(str(cellMomentsNormalized))
    cellMomentsNormalized00 = cellMomentsNormalizedDictionary["_0_0"]
    cellMomentsNormalized01 = cellMomentsNormalizedDictionary["_0_1"]
    cellMomentsNormalized02 = cellMomentsNormalizedDictionary["_0_2"]
    cellMomentsNormalized10 = cellMomentsNormalizedDictionary["_1_0"]
    cellMomentsNormalized11 = cellMomentsNormalizedDictionary["_1_1"]
    cellMomentsNormalized12 = cellMomentsNormalizedDictionary["_1_2"]
    cellMomentsNormalized20 = cellMomentsNormalizedDictionary["_2_0"]
    cellMomentsNormalized21 = cellMomentsNormalizedDictionary["_2_1"]
    cellMomentsNormalized22 = cellMomentsNormalizedDictionary["_2_2"]

    cellMomentsSpatial = cellMomentsDictionary["spatial"]
    cellMomentsSpatialDictionary = eval(str(cellMomentsSpatial))
    cellMomentsSpatial00 = cellMomentsSpatialDictionary["_0_0"]
    cellMomentsSpatial01 = cellMomentsSpatialDictionary["_0_1"]
    cellMomentsSpatial02 = cellMomentsSpatialDictionary["_0_2"]
    cellMomentsSpatial10 = cellMomentsSpatialDictionary["_1_0"]
    cellMomentsSpatial11 = cellMomentsSpatialDictionary["_1_1"]
    cellMomentsSpatial12 = cellMomentsSpatialDictionary["_1_2"]
    cellMomentsSpatial20 = cellMomentsSpatialDictionary["_2_0"]
    cellMomentsSpatial21 = cellMomentsSpatialDictionary["_2_1"]
    cellMomentsSpatial22 = cellMomentsSpatialDictionary["_2_2"]

    cellMomentsWeightedCentral = cellMomentsDictionary["weighted_central"]
    cellMomentsWeightedCentralDictionary = eval(str(cellMomentsWeightedCentral))
    cellMomentsWeightedCentral00 = cellMomentsWeightedCentralDictionary["_0_0"]
    cellMomentsWeightedCentral01 = cellMomentsWeightedCentralDictionary["_0_1"]
    cellMomentsWeightedCentral02 = cellMomentsWeightedCentralDictionary["_0_2"]
    cellMomentsWeightedCentral10 = cellMomentsWeightedCentralDictionary["_1_0"]
    cellMomentsWeightedCentral11 = cellMomentsWeightedCentralDictionary["_1_1"]
    cellMomentsWeightedCentral12 = cellMomentsWeightedCentralDictionary["_1_2"]
    cellMomentsWeightedCentral20 = cellMomentsWeightedCentralDictionary["_2_0"]
    cellMomentsWeightedCentral21 = cellMomentsWeightedCentralDictionary["_2_1"]
    cellMomentsWeightedCentral22 = cellMomentsWeightedCentralDictionary["_2_2"]

    cellMomentsWeightedNormalized = cellMomentsDictionary["weighted_normalized"]
    cellMomentsWeightedNormalizedDictionary = eval(str(cellMomentsWeightedNormalized))
    cellMomentsWeightedNormalized00 = cellMomentsWeightedNormalizedDictionary["_0_0"]
    cellMomentsWeightedNormalized01 = cellMomentsWeightedNormalizedDictionary["_0_1"]
    cellMomentsWeightedNormalized02 = cellMomentsWeightedNormalizedDictionary["_0_2"]
    cellMomentsWeightedNormalized10 = cellMomentsWeightedNormalizedDictionary["_1_0"]
    cellMomentsWeightedNormalized11 = cellMomentsWeightedNormalizedDictionary["_1_1"]
    cellMomentsWeightedNormalized12 = cellMomentsWeightedNormalizedDictionary["_1_2"]
    cellMomentsWeightedNormalized20 = cellMomentsWeightedNormalizedDictionary["_2_0"]
    cellMomentsWeightedNormalized21 = cellMomentsWeightedNormalizedDictionary["_2_1"]
    cellMomentsWeightedNormalized22 = cellMomentsWeightedNormalizedDictionary["_2_2"]

    cellMomentsWeightedSpatial = cellMomentsDictionary["weighted_spatial"]
    cellMomentsWeightedSpatialDictionary = eval(str(cellMomentsWeightedSpatial))
    cellMomentsWeightedSpatial00 = cellMomentsWeightedSpatialDictionary["_0_0"]
    cellMomentsWeightedSpatial01 = cellMomentsWeightedSpatialDictionary["_0_1"]
    cellMomentsWeightedSpatial02 = cellMomentsWeightedSpatialDictionary["_0_2"]
    cellMomentsWeightedSpatial10 = cellMomentsWeightedSpatialDictionary["_1_0"]
    cellMomentsWeightedSpatial11 = cellMomentsWeightedSpatialDictionary["_1_1"]
    cellMomentsWeightedSpatial12 = cellMomentsWeightedSpatialDictionary["_1_2"]
    cellMomentsWeightedSpatial20 = cellMomentsWeightedSpatialDictionary["_2_0"]
    cellMomentsWeightedSpatial21 = cellMomentsWeightedSpatialDictionary["_2_1"]
    cellMomentsWeightedSpatial22 = cellMomentsWeightedSpatialDictionary["_2_2"]
    cellMomentsArray = list(cellMomentsCentralDictionary.values())
    cellMomentsArray += list(cellMomentsHuDictionary.values())
    cellMomentsArray += list(cellMomentsHuWeightedDictionary.values())
    cellMomentsArray += list(cellMomentsNormalizedDictionary.values())
    cellMomentsArray += list(cellMomentsSpatialDictionary.values())
    cellMomentsArray += list(cellMomentsWeightedCentralDictionary.values())
    cellMomentsArray += list(cellMomentsWeightedNormalizedDictionary.values())
    cellMomentsArray += list(cellMomentsWeightedSpatialDictionary.values())

    cellOrientation = [cellDictionary["orientation"]]

    cellPerimeter = [cellDictionary["perimeter"]]

    cellShannon = cellDictionary["shannon_entropy"]
    cellShannonDictionary = eval(str(cellShannon))
    cellShannonHartley = cellShannonDictionary["hartley"]
    cellShannonNatural = cellShannonDictionary["natural"]
    cellShannonShannon = cellShannonDictionary["shannon"]
    cellShannonArray = list(cellShannonDictionary.values())

    cellSolidity = [cellDictionary["solidity"]]

    cellZernike = cellDictionary["moments_zernike"]
    cellZernikeDictionary = eval(str(cellZernike))
    cellZernike0 = cellZernikeDictionary["_0"]
    cellZernike1 = cellZernikeDictionary["_1"]
    cellZernike2 = cellZernikeDictionary["_2"]
    cellZernike3 = cellZernikeDictionary["_3"]
    cellZernike4 = cellZernikeDictionary["_4"]
    cellZernike5 = cellZernikeDictionary["_5"]
    cellZernike6 = cellZernikeDictionary["_6"]
    cellZernike7 = cellZernikeDictionary["_7"]
    cellZernike8 = cellZernikeDictionary["_8"]
    cellZernike9 = cellZernikeDictionary["_9"]
    cellZernike10 = cellZernikeDictionary["_10"]
    cellZernike11 = cellZernikeDictionary["_11"]
    cellZernike12 = cellZernikeDictionary["_12"]
    cellZernike13 = cellZernikeDictionary["_13"]
    cellZernike14 = cellZernikeDictionary["_14"]
    cellZernike15 = cellZernikeDictionary["_15"]
    cellZernike16 = cellZernikeDictionary["_16"]
    cellZernike17 = cellZernikeDictionary["_17"]
    cellZernike18 = cellZernikeDictionary["_18"]
    cellZernike19 = cellZernikeDictionary["_19"]
    cellZernike20 = cellZernikeDictionary["_20"]
    cellZernike21 = cellZernikeDictionary["_21"]
    cellZernike22 = cellZernikeDictionary["_22"]
    cellZernike23 = cellZernikeDictionary["_23"]
    cellZernike24 = cellZernikeDictionary["_24"]
    cellZernikeArray = list(cellZernikeDictionary.values())


    cellThreshold = cellDictionary["threshold_adjacency_statistics"]
    cellThresholdDictionary = eval(str(cellThreshold))
    cellThreshold0 = cellThresholdDictionary["_0"]
    cellThreshold1 = cellThresholdDictionary["_1"]
    cellThreshold2 = cellThresholdDictionary["_2"]
    cellThreshold3 = cellThresholdDictionary["_3"]
    cellThreshold4 = cellThresholdDictionary["_4"]
    cellThreshold5 = cellThresholdDictionary["_5"]
    cellThreshold6 = cellThresholdDictionary["_6"]
    cellThreshold7 = cellThresholdDictionary["_7"]
    cellThreshold8 = cellThresholdDictionary["_8"]
    cellThreshold9 = cellThresholdDictionary["_9"]
    cellThreshold10 = cellThresholdDictionary["_10"]
    cellThreshold11 = cellThresholdDictionary["_11"]
    cellThreshold12 = cellThresholdDictionary["_12"]
    cellThreshold13 = cellThresholdDictionary["_13"]
    cellThreshold14 = cellThresholdDictionary["_14"]
    cellThreshold15 = cellThresholdDictionary["_15"]
    cellThreshold16 = cellThresholdDictionary["_16"]
    cellThreshold17 = cellThresholdDictionary["_17"]
    cellThreshold18 = cellThresholdDictionary["_18"]
    cellThreshold19 = cellThresholdDictionary["_19"]
    cellThreshold20 = cellThresholdDictionary["_20"]
    cellThreshold21 = cellThresholdDictionary["_21"]
    cellThreshold22 = cellThresholdDictionary["_22"]
    cellThreshold23 = cellThresholdDictionary["_23"]
    cellThreshold24 = cellThresholdDictionary["_24"]
    cellThreshold25 = cellThresholdDictionary["_25"]
    cellThreshold26 = cellThresholdDictionary["_26"]
    cellThreshold27 = cellThresholdDictionary["_27"]
    cellThreshold28 = cellThresholdDictionary["_28"]
    cellThreshold29 = cellThresholdDictionary["_29"]
    cellThreshold30 = cellThresholdDictionary["_30"]
    cellThreshold31 = cellThresholdDictionary["_31"]
    cellThreshold32 = cellThresholdDictionary["_32"]
    cellThreshold33 = cellThresholdDictionary["_33"]
    cellThreshold34 = cellThresholdDictionary["_34"]
    cellThreshold35 = cellThresholdDictionary["_35"]
    cellThreshold36 = cellThresholdDictionary["_36"]
    cellThreshold37 = cellThresholdDictionary["_37"]
    cellThreshold38 = cellThresholdDictionary["_38"]
    cellThreshold39 = cellThresholdDictionary["_39"]
    cellThreshold40 = cellThresholdDictionary["_40"]
    cellThreshold41 = cellThresholdDictionary["_41"]
    cellThreshold42 = cellThresholdDictionary["_42"]
    cellThreshold43 = cellThresholdDictionary["_43"]
    cellThreshold44 = cellThresholdDictionary["_44"]
    cellThreshold45 = cellThresholdDictionary["_45"]
    cellThreshold46 = cellThresholdDictionary["_46"]
    cellThreshold47 = cellThresholdDictionary["_47"]
    cellThreshold48 = cellThresholdDictionary["_48"]
    cellThreshold49 = cellThresholdDictionary["_49"]
    cellThreshold50 = cellThresholdDictionary["_50"]
    cellThreshold51 = cellThresholdDictionary["_51"]
    cellThreshold52 = cellThresholdDictionary["_52"]
    cellThreshold53 = cellThresholdDictionary["_53"]
    cellThresholdArray = list(cellThresholdDictionary.values())

    cellPatterns = cellDictionary["local_binary_patterns"]
    cellPatternsDictionary = eval(str(cellPatterns))
    cellPatterns0 = cellPatternsDictionary["_0"]
    cellPatterns1 = cellPatternsDictionary["_1"]
    cellPatterns2 = cellPatternsDictionary["_2"]
    cellPatterns3 = cellPatternsDictionary["_3"]
    cellPatterns4 = cellPatternsDictionary["_4"]
    cellPatterns5 = cellPatternsDictionary["_5"]
    cellPatterns6 = cellPatternsDictionary["_6"]
    cellPatterns7 = cellPatternsDictionary["_7"]
    cellPatterns8 = cellPatternsDictionary["_8"]
    cellPatterns9 = cellPatternsDictionary["_9"]
    cellPatterns10 = cellPatternsDictionary["_10"]
    cellPatterns11 = cellPatternsDictionary["_11"]
    cellPatterns12 = cellPatternsDictionary["_12"]
    cellPatterns13 = cellPatternsDictionary["_13"]
    cellPatternsArray = list(cellPatternsDictionary.values())

    cellHaralick = cellDictionary["haralick"]
    cellHaralickDictionary = eval(str(cellHaralick))
    cellHaralick0 = cellHaralickDictionary["_0"]
    cellHaralick0Dictionary = eval(str(cellHaralick0))
    cellHaralick90 = cellHaralickDictionary["_90"]
    cellHaralick90Dictionary = eval(str(cellHaralick90))
    cellHaralick180 = cellHaralickDictionary["_180"]
    cellHaralick180Dictionary = eval(str(cellHaralick180))
    cellHaralick270 = cellHaralickDictionary["_270"]
    cellHaralick270Dictionary = eval(str(cellHaralick270))

    cellHaralick0AngularSecondMoment = cellHaralick0Dictionary["angular_second_moment"]
    cellHaralick0Contrast = cellHaralick0Dictionary["contrast"]
    cellHaralick0Correlation = cellHaralick0Dictionary["correlation"]
    cellHaralick0SSVariance = cellHaralick0Dictionary["ss_variance"]
    cellHaralick0InverseDifferenceMoment = cellHaralick0Dictionary["inverse_difference_moment"]
    cellHaralick0SumAverage = cellHaralick0Dictionary["sum_average"]
    cellHaralick0SumVariance = cellHaralick0Dictionary["sum_variance"]
    cellHaralick0SumEntropy = cellHaralick0Dictionary["sum_entropy"]
    cellHaralick0Entropy = cellHaralick0Dictionary["entropy"]
    cellHaralick0DifferenceVariance = cellHaralick0Dictionary["difference_variance"]
    cellHaralick0DifferenceEntropy = cellHaralick0Dictionary["difference_entropy"]
    cellHaralick0InformationMeasureOfCorrelation1 = cellHaralick0Dictionary["information_measure_of_correlation_1"]
    cellHaralick0InformationMeasureOfCorrelation2 = cellHaralick0Dictionary["information_measure_of_correlation_2"]

    cellHaralick90AngularSecondMoment = cellHaralick90Dictionary["angular_second_moment"]
    cellHaralick90Contrast = cellHaralick90Dictionary["contrast"]
    cellHaralick90Correlation = cellHaralick90Dictionary["correlation"]
    cellHaralick90SSVariance = cellHaralick90Dictionary["ss_variance"]
    cellHaralick90InverseDifferenceMoment = cellHaralick90Dictionary["inverse_difference_moment"]
    cellHaralick90SumAverage = cellHaralick90Dictionary["sum_average"]
    cellHaralick90SumVariance = cellHaralick90Dictionary["sum_variance"]
    cellHaralick90SumEntropy = cellHaralick90Dictionary["sum_entropy"]
    cellHaralick90Entropy = cellHaralick90Dictionary["entropy"]
    cellHaralick90DifferenceVariance = cellHaralick90Dictionary["difference_variance"]
    cellHaralick90DifferenceEntropy = cellHaralick90Dictionary["difference_entropy"]
    cellHaralick90InformationMeasureOfCorrelation1 = cellHaralick90Dictionary["information_measure_of_correlation_1"]
    cellHaralick90InformationMeasureOfCorrelation2 = cellHaralick90Dictionary["information_measure_of_correlation_2"]

    cellHaralick180AngularSecondMoment = cellHaralick180Dictionary["angular_second_moment"]
    cellHaralick180Contrast = cellHaralick180Dictionary["contrast"]
    cellHaralick180Correlation = cellHaralick180Dictionary["correlation"]
    cellHaralick180SSVariance = cellHaralick180Dictionary["ss_variance"]
    cellHaralick180InverseDifferenceMoment = cellHaralick180Dictionary["inverse_difference_moment"]
    cellHaralick180SumAverage = cellHaralick180Dictionary["sum_average"]
    cellHaralick180SumVariance = cellHaralick180Dictionary["sum_variance"]
    cellHaralick180SumEntropy = cellHaralick180Dictionary["sum_entropy"]
    cellHaralick180Entropy = cellHaralick180Dictionary["entropy"]
    cellHaralick180DifferenceVariance = cellHaralick180Dictionary["difference_variance"]
    cellHaralick180DifferenceEntropy = cellHaralick180Dictionary["difference_entropy"]
    cellHaralick180InformationMeasureOfCorrelation1 = cellHaralick180Dictionary["information_measure_of_correlation_1"]
    cellHaralick180InformationMeasureOfCorrelation2 = cellHaralick180Dictionary["information_measure_of_correlation_2"]

    cellHaralick270AngularSecondMoment = cellHaralick270Dictionary["angular_second_moment"]
    cellHaralick270Contrast = cellHaralick270Dictionary["contrast"]
    cellHaralick270Correlation = cellHaralick270Dictionary["correlation"]
    cellHaralick270SSVariance = cellHaralick270Dictionary["ss_variance"]
    cellHaralick270InverseDifferenceMoment = cellHaralick270Dictionary["inverse_difference_moment"]
    cellHaralick270SumAverage = cellHaralick270Dictionary["sum_average"]
    cellHaralick270SumVariance = cellHaralick270Dictionary["sum_variance"]
    cellHaralick270SumEntropy = cellHaralick270Dictionary["sum_entropy"]
    cellHaralick270Entropy = cellHaralick270Dictionary["entropy"]
    cellHaralick270DifferenceVariance = cellHaralick270Dictionary["difference_variance"]
    cellHaralick270DifferenceEntropy = cellHaralick270Dictionary["difference_entropy"]
    cellHaralick270InformationMeasureOfCorrelation1 = cellHaralick270Dictionary["information_measure_of_correlation_1"]
    cellHaralick270InformationMeasureOfCorrelation2 = cellHaralick270Dictionary["information_measure_of_correlation_2"]
    cellHaralickArray = list(cellHaralick0Dictionary.values())
    cellHaralickArray += list(cellHaralick90Dictionary.values())
    cellHaralickArray += list(cellHaralick180Dictionary.values())
    cellHaralickArray += list(cellHaralick270Dictionary.values())

    newCellCreated = cellArea
    newCellCreated += cellBoundArray + cellCentroidArray + cellConvex + cellEccentricity + cellDiameter + cellEuler + cellExtent + cellInertiaArray + cellIntensityArray + cellLabel
    newCellCreated += cellMajor + cellMinor + cellMomentsArray + cellOrientation + cellPerimeter + cellShannonArray
    newCellCreated += cellSolidity + cellZernikeArray + cellThresholdArray + cellPatternsArray + cellHaralickArray + cellImage

    return newCellCreated

    # print(cellDictionary.keys())


def getNumberOfCells(filename):
    query = gql(
        """
        {
            find(type: Filename, arcql: "hypi.id = \'""" + filename + """\'"){
                edges {
                    node {
                        ... on Filename {
                            totalnumber
                        }
                    }
                }
            }
        }
        """
    )

    return client.execute(query)

def getEntries(filename):
    query = str(getNumberOfCells(filename))
    locnumber = query.find("'totalnumber': ")
    locend = query.find("}", locnumber)
    numEntries = int(query[(locnumber + len("'totalnumber': ")):locend])

    return numEntries



def retrievecells(filename):
    cellarray = []
    numberofentries = getEntries(filename)
    counter = 1
    while(counter < numberofentries):
        if(numberofentries - counter >= 3):
            toCheck = 3
        else:
            toCheck = numberofentries - counter
        stringfromquery = str(findcells(filename, toCheck, counter))
        # print(stringfromquery)
        for i in range(toCheck):
            loccurnode = stringfromquery.find("'node':")
            locnextnode = stringfromquery.find("'node':", loccurnode + 1)
            strnode = stringfromquery[loccurnode + 8: locnextnode - 4]
            # print(strnode)
            if(locnextnode != -1):
                currentcell = makecell(strnode)
            else:
                currentcell = makecell(stringfromquery[loccurnode + 8: len(stringfromquery) - 4])
            cellarray.append(currentcell)
            stringfromquery = stringfromquery[locnextnode:]
            # print(toCheck + counter)
        counter += toCheck
    return cellarray



def createFile(inputfile, outputfile):

    fieldnames = ['classification', 'area', 'bounding_box_area', 'bounding_box_maximum_column', 'bounding_box_maximum_row', 'bounding_box_minimum_column', 'bounding_box_minimum_row', 'centroid_column', 'centroid_row', 'centroid_weighted_column',
                  'centroid_weighted_local_column', 'centroid_weighted_local_row', 'centroid_weighted_row', 'convex_hull_area', 'eccentricity', 'equivalent_diameter', 'euler_number', 'extent', 'inertia_tensor_0_0', 'inertia_tensor_0_1',
                  'inertia_tensor_1_0', 'inertia_tensor_1_1', 'inertia_tensor_eigen_values_0', 'inertia_tensor_eigen_values_1', 'intensity_integrated', 'intensity_maximum', 'intensity_mean', 'intensity_median', 'intensity_median_absolute_deviation',
                  'intensity_minimum', 'intensity_quartile_1', 'intensity_quartile_2', 'intensity_quartile_3', 'intensity_standard_deviation', 'label', 'major_axis_length', 'minor_axis_length', 'moments_central_0_0', 'moments_central_0_1',
                  'moments_central_0_2', 'moments_central_1_0', 'moments_central_1_1', 'moments_central_1_2', 'moments_central_2_0', 'moments_central_2_1', 'moments_central_2_2', 'moments_hu_0', 'moments_hu_1', 'moments_hu_2', 'moments_hu_3',
                  'moments_hu_4', 'moments_hu_5', 'moments_hu_6', 'moments_hu_weighted_0', 'moments_hu_weighted_1', 'moments_hu_weighted_2', 'moments_hu_weighted_3', 'moments_hu_weighted_4', 'moments_hu_weighted_5', 'moments_hu_weighted_6',
                  'moments_normalized_0_0', 'moments_normalized_0_1', 'moments_normalized_0_2', 'moments_normalized_1_0', 'moments_normalized_1_1', 'moments_normalized_1_2', 'moments_normalized_2_0', 'moments_normalized_2_1', 'moments_normalized_2_2',
                  'moments_spatial_0_0', 'moments_spatial_0_1', 'moments_spatial_0_2', 'moments_spatial_1_0', 'moments_spatial_1_1', 'moments_spatial_1_2', 'moments_spatial_2_0', 'moments_spatial_2_1', 'moments_spatial_2_2', 'moments_weighted_central_0_0',
                  'moments_weighted_central_0_1', 'moments_weighted_central_0_2', 'moments_weighted_central_1_0', 'moments_weighted_central_1_1', 'moments_weighted_central_1_2', 'moments_weighted_central_2_0', 'moments_weighted_central_2_1',
                  'moments_weighted_central_2_2', 'moments_weighted_normalized_0_0', 'moments_weighted_normalized_0_1', 'moments_weighted_normalized_0_2', 'moments_weighted_normalized_1_0', 'moments_weighted_normalized_1_1', 'moments_weighted_normalized_1_2',
                  'moments_weighted_normalized_2_0', 'moments_weighted_normalized_2_1', 'moments_weighted_normalized_2_2', 'moments_weighted_spatial_0_0', 'moments_weighted_spatial_0_1', 'moments_weighted_spatial_0_2', 'moments_weighted_spatial_1_0',
                  'moments_weighted_spatial_1_1', 'moments_weighted_spatial_1_2', 'moments_weighted_spatial_2_0', 'moments_weighted_spatial_2_1', 'moments_weighted_spatial_2_2', 'orientation', 'perimeter', 'shannon_entropy_hartley', 'shannon_entropy_natural',
                  'shannon_entropy_shannon', 'solidity', 'moments_zernike_8_8_00', 'moments_zernike_8_8_01', 'moments_zernike_8_8_02', 'moments_zernike_8_8_03', 'moments_zernike_8_8_04', 'moments_zernike_8_8_05', 'moments_zernike_8_8_06', 'moments_zernike_8_8_07',
                  'moments_zernike_8_8_08', 'moments_zernike_8_8_09', 'moments_zernike_8_8_10', 'moments_zernike_8_8_11', 'moments_zernike_8_8_12', 'moments_zernike_8_8_13', 'moments_zernike_8_8_14', 'moments_zernike_8_8_15', 'moments_zernike_8_8_16',
                  'moments_zernike_8_8_17', 'moments_zernike_8_8_18', 'moments_zernike_8_8_19', 'moments_zernike_8_8_20', 'moments_zernike_8_8_21', 'moments_zernike_8_8_22', 'moments_zernike_8_8_23', 'moments_zernike_8_8_24', 'threshold_adjacency_statistics_00',
                  'threshold_adjacency_statistics_01', 'threshold_adjacency_statistics_02', 'threshold_adjacency_statistics_03', 'threshold_adjacency_statistics_04', 'threshold_adjacency_statistics_05', 'threshold_adjacency_statistics_06',
                  'threshold_adjacency_statistics_07', 'threshold_adjacency_statistics_08', 'threshold_adjacency_statistics_09', 'threshold_adjacency_statistics_10', 'threshold_adjacency_statistics_11', 'threshold_adjacency_statistics_12',
                  'threshold_adjacency_statistics_13', 'threshold_adjacency_statistics_14', 'threshold_adjacency_statistics_15', 'threshold_adjacency_statistics_16', 'threshold_adjacency_statistics_17', 'threshold_adjacency_statistics_18',
                  'threshold_adjacency_statistics_19', 'threshold_adjacency_statistics_20', 'threshold_adjacency_statistics_21', 'threshold_adjacency_statistics_22', 'threshold_adjacency_statistics_23', 'threshold_adjacency_statistics_24',
                  'threshold_adjacency_statistics_25', 'threshold_adjacency_statistics_26', 'threshold_adjacency_statistics_27', 'threshold_adjacency_statistics_28', 'threshold_adjacency_statistics_29', 'threshold_adjacency_statistics_30',
                  'threshold_adjacency_statistics_31', 'threshold_adjacency_statistics_32', 'threshold_adjacency_statistics_33', 'threshold_adjacency_statistics_34', 'threshold_adjacency_statistics_35', 'threshold_adjacency_statistics_36',
                  'threshold_adjacency_statistics_37', 'threshold_adjacency_statistics_38', 'threshold_adjacency_statistics_39', 'threshold_adjacency_statistics_40', 'threshold_adjacency_statistics_41', 'threshold_adjacency_statistics_42',
                  'threshold_adjacency_statistics_43', 'threshold_adjacency_statistics_44', 'threshold_adjacency_statistics_45', 'threshold_adjacency_statistics_46', 'threshold_adjacency_statistics_47', 'threshold_adjacency_statistics_48',
                  'threshold_adjacency_statistics_49', 'threshold_adjacency_statistics_50', 'threshold_adjacency_statistics_51', 'threshold_adjacency_statistics_52', 'threshold_adjacency_statistics_53', 'local_binary_patterns_00_08_06',
                  'local_binary_patterns_01_08_06', 'local_binary_patterns_02_08_06', 'local_binary_patterns_03_08_06', 'local_binary_patterns_04_08_06', 'local_binary_patterns_05_08_06', 'local_binary_patterns_06_08_06', 'local_binary_patterns_07_08_06',
                  'local_binary_patterns_08_08_06', 'local_binary_patterns_09_08_06', 'local_binary_patterns_10_08_06', 'local_binary_patterns_11_08_06', 'local_binary_patterns_12_08_06', 'local_binary_patterns_13_08_06', 'haralick_angular_second_moment_8_000',
                  'haralick_contrast_8_000', 'haralick_correlation_8_000', 'haralick_sum_of_squares_variance_8_000', 'haralick_inverse_difference_moment_8_000', 'haralick_sum_average_8_000', 'haralick_sum_variance_8_000', 'haralick_sum_entropy_8_000',
                  'haralick_entropy_8_000', 'haralick_difference_variance_8_000', 'haralick_difference_entropy_8_000', 'haralick_information_measure_of_correlation_1_8_000', 'haralick_information_measure_of_correlation_2_8_000',
                  'haralick_angular_second_moment_8_090', 'haralick_contrast_8_090', 'haralick_correlation_8_090', 'haralick_sum_of_squares_variance_8_090', 'haralick_inverse_difference_moment_8_090', 'haralick_sum_average_8_090', 'haralick_sum_variance_8_090',
                  'haralick_sum_entropy_8_090', 'haralick_entropy_8_090', 'haralick_difference_variance_8_090', 'haralick_difference_entropy_8_090', 'haralick_information_measure_of_correlation_1_8_090', 'haralick_information_measure_of_correlation_2_8_090',
                  'haralick_angular_second_moment_8_180', 'haralick_contrast_8_180', 'haralick_correlation_8_180', 'haralick_sum_of_squares_variance_8_180', 'haralick_inverse_difference_moment_8_180', 'haralick_sum_average_8_180', 'haralick_sum_variance_8_180',
                  'haralick_sum_entropy_8_180', 'haralick_entropy_8_180', 'haralick_difference_variance_8_180', 'haralick_difference_entropy_8_180', 'haralick_information_measure_of_correlation_1_8_180', 'haralick_information_measure_of_correlation_2_8_180',
                  'haralick_angular_second_moment_8_270', 'haralick_contrast_8_270', 'haralick_correlation_8_270', 'haralick_sum_of_squares_variance_8_270', 'haralick_inverse_difference_moment_8_270', 'haralick_sum_average_8_270', 'haralick_sum_variance_8_270',
                  'haralick_sum_entropy_8_270', 'haralick_entropy_8_270', 'haralick_difference_variance_8_270', 'haralick_difference_entropy_8_270', 'haralick_information_measure_of_correlation_1_8_270', 'haralick_information_measure_of_correlation_2_8_270',
                  'pathname']
    rows = retrievecells(inputfile)
    with open(outputfile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(rows)


def delete(filename):
    numberofentries = getEntries(filename)
    counter = 1
    while (counter < numberofentries):
        if (numberofentries - counter >= 3):
            toCheck = 3
        else:
            toCheck = numberofentries - counter
        deletehelper(filename, toCheck, counter)
        counter += toCheck


def deletehelper(filename, no, current):
    query = gql(
        """
                mutation {
  delete(type: Cell, arcql: "filename = \'""" + filename + """\' AND row IN [""" + str(current) + ", " + str(current+no) + """)")
}
                        """
    )

    deletehelper2(filename, no)

    return client.execute(query)


def deletehelper2(filename, no):
    numentries = getEntries(filename)
    numleft = numentries - no
    if(numleft > 0):
        query = gql(
            """
            mutation UpdateNumEntries{
                upsert(values: {
                    Filename: [
                      {
                        hypi: {id: \"""" + filename + """\"},
                        csvname: \"""" + filename + """\",
                        totalnumber: """ + str(numleft) + """
                      }
                    ]
                }){id}
            }
            """

        )
    else:
        query = gql(
            """
            mutation {
                delete(type: Filename, arcql: "hypi.id = \'""" + filename + """\')
            }
            """

        )

    return client.execute(query)



def createcell_original(no, arr, filename):
  s = str(no)
  slashloc = str(filename).rfind("/")
  if(slashloc == -1):
      slashloc = str(filename).rfind("\\")
  csvloc = str(filename).rfind(".csv")
  filenamestr = str(filename)[slashloc+1:csvloc+4]
  finalid = filenamestr + s
  print(finalid)
  onecell = one_cell_original(arr,finalid)
  # print(onecell)
  query = gql(
        """
        mutation AddCells {
          upsert(values:{
            Cell:[
                {
                  """         
          + onecell +
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
  result = client.execute(query)
  print("done")


def createcell(no, arr, filename):
  
    s = str(no)
    slashloc = str(filename).rfind("/")
    if(slashloc == -1):
        slashloc = str(filename).rfind("\\")
    csvloc = str(filename).rfind(".csv")
    filenamestr = str(filename)[slashloc+1:csvloc+4]
    finalid = filenamestr + s
    print(finalid)
    # print(onecell)
    query = gql(
          """
          mutation AddCells {
            upsert(values:{
              Cell:[
                {
                  hypi: {id: \"""" + finalid + """\"}
              }
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
    result = client.execute(query)
    
    onecell = one_cell(arr, finalid)
    
    for queries in onecell:
      query2 = gql(
           """
          mutation UpdateCells {
            upsert(values:{
              Cell:[
                {
                  hypi: {id: \"""" + finalid + """\"},
                  """         
          + queries +
          """   }
        ]
        }){id}
      }
      """)
      print(queries)
      resultUpdate = client.execute(query2)
      # print("donePartly")
        
    #print(onecell)
    
    print("done")


# print(create_cell(skopy_data))
# createFile("features.csv", "test.csv")
# print(getFiles())
# print(findcells("features.csv"))
# while(True):
#     print(delete())
# print(delete("features.csv"))
# print(len(retrievecells("features.csv")))
# test_mutation_result(client)
# test_get(client)
# filename = "features.csv"
# print(retrievecells(filename))



# print("hi")
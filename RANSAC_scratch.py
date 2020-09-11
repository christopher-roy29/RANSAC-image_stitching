
import random
def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    For example: If 'a','b' is inlier_points and 'c' is outlier_point.
    the output should be two lists of ['a', 'b'], ['c'].
    Note that, these two lists should be non-empty.
    """
    random.seed(a=26)
    inlier_points_name = []; outlier_points_name = []; least_error = 1000; in_point_prev= [];
    for i in range(k):
        while True:
            in_point1 = (random.choice(input_points)).get('value')
            in_point2 = (random.choice(input_points)).get('value')
            if in_point1 != in_point2 and ([in_point1,in_point2] not in in_point_prev):
                break;

        # if(in_point1 != in_point2 and [in_point1,in_point2] not in in_point_prev):
        try:
            slope = (in_point1[1] - in_point2[1]) / (in_point1[0] - in_point2[0])
        except ZeroDivisionError:
            slope = 0;
        try:
            intercept = (in_point1[0] * in_point2[1] - in_point2[0] * in_point1[1]) / (in_point1[0] - in_point2[0])
        except ZeroDivisionError:
            intercept = 0;
        inliers = []; outliers = [];
        xyz = [v for k,v in enumerate(input_points) if (v.get('value') != in_point1 and v.get('value') != in_point2)]
        error = 0
        for j in xyz:
            dist = abs(((slope * j.get('value')[0]) - j.get('value')[1] + intercept) / ((slope * slope) + 1)**0.5)
            if(dist<t):
                inliers.append(j)
            else:
                outliers.append(j)
        if(len(inliers)>d):
            for j in inliers:
                dist_i = abs(((slope * j.get('value')[0]) - j.get('value')[1] + intercept) / ((slope * slope) + 1) ** 0.5)
                error += dist_i
            error = error / len(inliers)
            if(error<least_error):
                inlier_points_name = []; outlier_points_name = [];
                for elem in inliers:
                    name = elem.get('name')
                    inlier_points_name.append(name)
                    #inlier_points_name = list(inliers.get('name')) + list(in_point1.get('name')) + list(in_point2.get('name'))
                in_p1 = [v.get('name') for k, v in enumerate(input_points) if (v.get('value') == in_point1 )]
                in_p2 = [v.get('name') for k, v in enumerate(input_points) if (v.get('value') == in_point2 )]
                inlier_points_name += in_p1;inlier_points_name += in_p2;
                for elem in outliers:
                    name = elem.get('name')
                    outlier_points_name.append(name)
                # outlier_points_name = list(outliers.get('name'))
                least_error = error
        in_point_prev.append([list(in_point1),list(in_point2)])

    #RETURN---- add the 2 points used to make the line, to inliers while returning inlier_points_name
    return inlier_points_name, outlier_points_name

if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k) 
    assert len(inlier_points_name) + len(outlier_points_name) == 8  
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()



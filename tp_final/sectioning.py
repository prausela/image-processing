import cv2
import numpy as np
import math

## PRIVATE FUNCTIONS ##

SECTION_VERTICAL = 0
SECTION_HORIZONTAL = 1
SECTION_LOWEST = 0
SECTION_HIGHEST = 1

def _ranges_intersect(
        limit_a: tuple[int, int],
        limit_b: tuple[int, int],
        tol: float
        ) -> bool:
    min_a, max_a = limit_a
    min_b, max_b = limit_b
    if min_a < min_b:
        return max_a+tol >= min_b
    else:
        return max_b+tol >= min_a
    
def _augment_range(
        limit_a: tuple[int, int],
        limit_b: tuple[int, int]
        ) -> tuple[int, int]:
    min_a, max_a = limit_a
    min_b, max_b = limit_b
    lowest_min = min(min_a, min_b)
    highest_max = max(max_a, max_b)
    return (lowest_min, highest_max)
    
def _sections_intersect(
        section_a: tuple[tuple[int, int], tuple[int, int]],
        section_b: tuple[tuple[int, int], tuple[int, int]],
        tol: float
        ) -> bool:
    vertical_limits_a, horizontal_limits_a = section_a
    vertical_limits_b, horizontal_limits_b = section_b
    return _ranges_intersect(horizontal_limits_a, horizontal_limits_b, tol) and _ranges_intersect(vertical_limits_a, vertical_limits_b, tol)

def _augment_section(
        section_a: tuple[tuple[int, int], tuple[int, int]],
        section_b: tuple[tuple[int, int], tuple[int, int]]
        ) -> tuple[tuple[int, int], tuple[int, int]]:
    vertical_limits_a, horizontal_limits_a = section_a
    vertical_limits_b, horizontal_limits_b = section_b
    new_vertical_limits = _augment_range(vertical_limits_a, vertical_limits_b)
    new_horizontal_limits = _augment_range(horizontal_limits_a, horizontal_limits_b)
    return (new_vertical_limits, new_horizontal_limits)
    

def _find_sections(canny_image: np.ndarray) -> tuple[list[tuple[tuple[int, int], tuple[int, int]]], np.ndarray]:
    contours, hierarchy = cv2.findContours(canny_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    square_sections_limits = []
    for contour in contours:
        highest = contour.max(axis=0)[0]
        lowest = contour.min(axis=0)[0]
        
        if highest[0] <= lowest[0]:
            continue
        if highest[1] <= lowest[1]:
            continue

        square_sections_limits.append(((lowest[1], (highest[1]+1)), (lowest[0], (highest[0]+1))))
    return square_sections_limits, hierarchy

def _sections_to_square_contours(sections_limits: np.ndarray) -> tuple:
    square_contours = []
    for section_limit in sections_limits:
        square_contours.append(
                np.array(
                    [
                        np.array([[section_limit[1][0], section_limit[0][0]]]),
                        np.array([[section_limit[1][0], section_limit[0][1]-1]]),
                        np.array([[section_limit[1][1]-1, section_limit[0][1]-1]]),
                        np.array([[section_limit[1][1]-1, section_limit[0][0]]]),
                        np.array([[section_limit[1][0], section_limit[0][0]]]),
                    ]
                )
            )
    square_contours = tuple(square_contours)
    return square_contours

## PUBLIC FUNCTIONS ##

def obtain_sections(
        canny_image: np.ndarray
        ) -> tuple[tuple[tuple[int, int], tuple[int, int]], np.ndarray]:
    canny_image_copy = canny_image.copy()
    square_sections_limits, hierarchy = _find_sections(canny_image_copy)
    return square_sections_limits, hierarchy

def draw_sections(
        canny_image: np.ndarray,
        sections_limits: list[tuple[tuple[int, int], tuple[int, int]]]
        ) -> np.ndarray:
    canny_image_copy = canny_image.copy()
    square_contours = _sections_to_square_contours(sections_limits)
    return cv2.drawContours(canny_image_copy, square_contours, -1, 255, 3)

def get_section(
        image: np.ndarray, 
        section_limits: tuple[tuple[int, int], tuple[int, int]]
        ) -> np.ndarray:
    return image[
        section_limits[SECTION_VERTICAL][SECTION_LOWEST]:section_limits[SECTION_VERTICAL][SECTION_HIGHEST], 
        section_limits[SECTION_HORIZONTAL][SECTION_LOWEST]:section_limits[SECTION_HORIZONTAL][SECTION_HIGHEST]
    ]

def sectionize_image(
        canny_image: np.ndarray, 
        sections_limits: list[tuple[tuple[int, int], tuple[int, int]]]
        ) -> list[np.ndarray]:
    sectionized_image = []
    for section_limits in sections_limits:
        sectionized_image.append(get_section(canny_image, section_limits))
    return sectionized_image

def merge_all_sections(
        sections_limits: list[tuple[tuple[int, int], tuple[int, int]]],
        tol: float = 0
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    
    have_intersected = True

    while have_intersected:
        have_intersected = False

        group_labels_aux = list(range(len(sections_limits)))
        for i in range(len(sections_limits)):
            for j in range(len(sections_limits)):
                if i != j and _sections_intersect(sections_limits[i], sections_limits[j], tol):
                    have_intersected = True
                    group_label = min(group_labels_aux[i], group_labels_aux[j])
                    group_labels_aux[i] = group_label
                    group_labels_aux[j] = group_label

        group_labels = set()
        for group_label in group_labels_aux:
            group_labels.add(group_label)

        new_sections_limits = []
        for group_label in group_labels:
            new_section_limits = None
            for i in range(len(group_labels_aux)):
                if group_labels_aux[i] == group_label:
                    if new_section_limits is None:
                        new_section_limits = sections_limits[i]
                    else:
                        new_section_limits = _augment_section(new_section_limits, sections_limits[i])
            new_sections_limits.append(new_section_limits)

        sections_limits = new_sections_limits
                    
    return new_sections_limits
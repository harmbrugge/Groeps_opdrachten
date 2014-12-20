__author__ = 'Olivier'

di_repeat_positions = di_search.span()
repeat_len = di_repeat_positions[1] - di_repeat_positions[0]
if not repeat_len % 3:

    repeat_count = (repeat_len/3) - self.nr_nuc_di_repeat

    if repeat_count > 0:
        skip_value = (di_repeat_positions[0] + repeat_count*3)
    else:
        skip_value = (di_repeat_positions[0] + 3)
    i += int(skip_value)

elif not repeat_len % 2:

    repeat_count = (repeat_len/2) - self.nr_nuc_di_repeat
    if repeat_count > 0:
        skip_value = (di_repeat_positions[0] + repeat_count*2)
    else:
        skip_value = (di_repeat_positions[0] + 2)

    i += int(skip_value)


# di_repeat_positions = di_search.span()
# repeat_len = di_repeat_positions[1] - di_repeat_positions[0]
# if not repeat_len % 3:
#
#     repeat_count = (repeat_len/3) - self.nr_nuc_di_repeat
#
#     if repeat_count > 0:
#         skip_value = (di_repeat_positions[0] + repeat_count*3)
#     else:
#         skip_value = (di_repeat_positions[0] + 3)
#     i += int(skip_value)
#
# elif not repeat_len % 2:
#
#     repeat_count = (repeat_len/2) - self.nr_nuc_di_repeat
#     if repeat_count > 0:
#         skip_value = (di_repeat_positions[0] + repeat_count*2)
#     else:
#         skip_value = (di_repeat_positions[0] + 2)
#
#     i += int(skip_value)


skip_value = mono_repeat_positions[1] - self.nr_nuc_mono_repeat
i += (skip_value-1)
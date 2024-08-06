from poster.models import Ticket


def hall_scheme(session):
    tickets = Ticket.objects.filter(session=session)

    seating_chart = {}
    for ticket in tickets:
        sector = ticket.seat.hall_sector.name
        row = ticket.seat.row
        place = ticket.seat.place
        if sector not in seating_chart:
            seating_chart[sector] = {}
        if row not in seating_chart[sector]:
            seating_chart[sector][row] = []

        seating_chart[sector][row].append({
            'place': place,
            'is_free': not (ticket.sold or ticket.reserved),
            'price': ticket.price,
            'x': calculate_x(ticket.seat),
            'y': calculate_y(ticket.seat),
        })
    return seating_chart


def calculate_y(seat):
    sector_y_offsets = {
        'партер': {
            range(1, 9): 0,
            range(9, 22): 40,
        },
        'балкон': {
            range(1, 6): 500,
        }
    }
    sector = sector_y_offsets.get(seat.hall_sector.name)
    if sector:
        for place_range, y_offset in sector.items():
            if seat.row in place_range:
                return seat.row * 20 + y_offset


def calculate_x(seat):
    sector_x_offsets = {
        'партер': {
            range(1, 2): {range(1, 11): 0, range(11, 100): 80},
            range(2, 9): {range(1, 12): 0, range(12, 100): 40},
            range(9, 18): {range(1, 7): 0, range(7, 15): 40, range(15, 100): 80},
            range(18, 21): {range(1, 5): 0, range(5, 11): 100, range(11, 100): 200},
            range(21, 22): {range(1, 6): 0, range(6, 12): 80, range(12, 100): 160}
        },
        'балкон': {
            range(1, 3): {range(1, 3): 0, range(3, 20): 30, range(20, 22): 60},
            range(3, 6): {range(1, 3): 0, range(3, 5): 400},
        }
    }

    sector = sector_x_offsets.get(seat.hall_sector.name)
    if sector:
        for row_range, place_offsets in sector.items():
            if seat.row in row_range:
                for place_range, x_offset in place_offsets.items():
                    if seat.place in place_range:
                        return seat.place * 20 + x_offset

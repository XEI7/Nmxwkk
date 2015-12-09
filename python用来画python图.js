/* Facilitate inheritence in JS */
Object.prototype.extend = function (parent) {
    for (p in parent) { if (!(p in this)) this[p] = parent[p]; }
}


/* Puzzle solver */
function PuzzleSolver(table, width, height, hConstraints, vConstraints) {
    this._width = width;
    this._height = height;
    this._grid = new Array();
    this._drawTable(table);
    this._lines = new Array();
    for (var i = 0; i < hConstraints.length; i++) {
        var indexes = new Array();
        for (var j = i * width; j < (i + 1) * width; j++)
            indexes.push(j);
        this._lines.push(new Line(this, hConstraints[i], width, indexes));
    }
    for (var i = 0; i < vConstraints.length; i++) {
        var indexes = new Array();
        for (var j = i; j < (height * width); j += width)
            indexes.push(j);
        this._lines.push(new Line(this, vConstraints[i], width, indexes));
    }
}

PuzzleSolver.prototype = {
    _grid: [],
    _width: 0,
    _height: 0,
    _lines: [],

    _drawTable: function(table) {
        var body = document.createElement('tbody');
        table.appendChild(body);

        // cells
        for (var j = 0; j < this._height; j++) {
            var row = document.createElement('tr');
            body.appendChild(row);
            for (var i = 0; i < this._width; i++) {
                var cell = document.createElement('td');
                cell.className = 'unsolved';
                cell.setAttribute('id', 'cell-' + i + '-' + j);
                row.appendChild(cell);
                this._grid.push(cell);
            }
        }
    },

    solve: function(name) {
        while (!this.isSolved()) this.solveStep();
    },

    solveStep: function(name) {
        for (var i = 0; i < this._lines.length; i++)
            this._lines[i].solve(this._grid);
    },

    isSolved: function() {
        for (var i = 0; i < this._grid.length; i++) {
            if (this._grid[i].className == 'unsolved')
                return false;
        }
        return true;
    }
}


/* Line in puzzle */
function Line(puzzle, constraints, length, indexes) {
    this._length = length;
    this._line = [];
    for (var i = 0; i < indexes.length; i++)
        this._line.push(puzzle._grid[indexes[i]]);

    var c = new Array();
    c.push(new StartBlanks(this));

    for (var i = 0; i < constraints.length; i++) {
        c.push(new Constraint(this, c.length, constraints[i]));
        c.push(new Blanks(this, c.length));
    }

    c.pop(); // last blanks
    c.push(new EndBlanks(this, c.length));
    this._constraints = c;
}

Line.prototype = {
    _constraints: [],
    _length: -1,
    _line: [],

    solve: function() {
        var groups = {
            'unsolved': new Array(),
            'off': new Array(),
            'on': new Array()
        };
        var current = 'unsolved';
        var start = -1;
        for (var i = 0; i < this._line.length; i++) {
            if (this._line[i].className != current) {
                if (start > -1)
                    groups[current].push([start, i]);
                start = i;
                current = this._line[i].className;
            }
        }
        if (start > -1)
            groups[current].push([start, this._line.length]);

        for (var i = 0; i < groups['on'].length; i++) {
            var group = groups['on'][i];
            var matches = new Array();
            for (var j = 0; j < this._constraints.length; j++) {
                var c = this._constraints[j];
                if (!c.isBlanks && c.matches(group[0], group[1]))
                    matches.push(c);
            }
            if (matches.length == 1)
                matches[0].assign(group[0], group[1]);
        }

        for (var i = 0; i < groups['off'].length; i++) {
            var group = groups['off'][i];
            var matches = new Array();
            for (var j = 0; j < this._constraints.length; j++) {
                var c = this._constraints[j];
                if (c.isBlanks && c.matches(group[0], group[1]))
                    matches.push(c);
            }
            if (matches.length == 1)
                matches[0].assign(group[0], group[1]);
        }

        for (var i = 0; i < this._constraints.length; i++)
            this._constraints[i].solve(this._line);
    }
}


/* A pixel constraint in a line */
function Constraint(line, index, length) {
    this._line = line;
    this._index = index;
    this._length = length;
}

Constraint.prototype = {
    _extend: [Number.MAX_VALUE, -1],
    _line: null,
    _index: -1,
    _length: -1,
    _solved: 'on',
    isBlanks: false,

    assign: function(start, stop) {
        this._extend = [Math.min(this._extend[0], start),
                        Math.max(this._extend[1], stop)];
    },

    next: function() {
        try {
            return this._line._constraints[this._index + 1];
        } catch (e) {
            return null;
        }
    },

    previous: function() {
        try {
            return this._line._constraints[this._index - 1];
        } catch (e) {
            return null;
        }
    },

    minLeft: function() {
        var left = 0;
        var prev = this.previous();
        if (prev != null)
            left = prev.minRight();
        return Math.max(left, this._extend[1] - this._length);
    },

    minRight: function() {
        return this.minLeft() + this._length;
    },

    maxLeft: function() {
        return this.maxRight() - this._length;
    },

    maxRight: function() {
        var right = this._line._length;
        var next = this.next();
        if (next != null)
            right = next.maxLeft();
        return Math.min(right, this._extend[0] + this._length);
    },

    minRightExpanded: function() { return this.minRight(); },
    maxLeftExpanded: function() { return this.maxLeft(); },

    matches: function(start, stop) {
        if ((stop - start) > this._length)
            return false;
        if (start >= this.minLeft() && stop <= this.maxRight())
            return true;
        return false;
    },

    solve: function(line) {
        var start = this.maxLeftExpanded();
        var stop = this.minRightExpanded();
        for (var i = start; i < stop; i++)
            line[i].className = this._solved;
    }
}


/* Blanks in a line */
function Blanks(line, index) {
    this.extend(new Constraint(line, index, -1));
}

Blanks.prototype = {
    _minLength: 1,
    _solved: 'off',
    isBlanks: true,

    minLeft: function() {
        var prev = this.previous();
        if (prev != null)
            return prev.minRight();
        return 0;
    },

    minRight: function() {
        return Math.max(this.minLeft() + this._minLength, this._extend[1]);
    },

    maxLeft: function() {
        return Math.min(this.maxRight() - this._minLength, this._extend[0]);
    },

    maxRight: function() {
        var next = this.next();
        if (next != null)
            return next.maxLeft();
        return this._line._length;
    },

    minRightExpanded: function() {
        var next = this.next();
        if (next != null)
            return Math.max(this.minRight(), next.minLeft());
        return this._line._length;
    },

    maxLeftExpanded: function() {
        var prev = this.previous();
        if (prev != null)
            return Math.min(this.maxLeft(), prev.maxRight());
        return 0;
    },

    matches: function(start, stop) {
        if (start >= this.minLeft() && stop <= this.maxRight())
            return true;
        return false;
    }
}


/* Blanks at the start of a line */
function StartBlanks(line) {
    this.extend(new Blanks(line, 0));
}

StartBlanks.prototype = {
    _minLength: 0,
    minLeft: function() { return 0; },
    maxLeft: function() { return 0; }
}


/* Blanks at the end of the line */
function EndBlanks(line, index) {
    this.extend(new Blanks(line, index));
}

EndBlanks.prototype = {
    _minLength: 0,
    minRight: function() { return this._line._length; },
    maxRight: function() { return this._line._length; }
}


var solver;
var animPause = 60;
hConstraints = [[3, 2], [8], [10], [3, 1, 1], [5, 2, 1], [5, 2, 1], [4, 1, 1],
    [15], [19], [6, 14], [6, 1, 12], [6, 1, 10], [7, 2, 1, 8],
    [6, 1, 1, 2, 1, 1, 1, 1], [5, 1, 4, 1], [5, 4, 1, 4, 1, 1, 1],
    [5, 1, 1, 8], [5, 2, 1, 8], [6, 1, 2, 1, 3], [6, 3, 2, 1], [6, 1, 5],
    [1, 6, 3], [2, 7, 2], [3, 3, 10, 4], [9, 12, 1], [22, 1], [21, 4],
    [1, 17, 1], [2, 8, 5, 1], [2, 2, 4], [5, 2, 1, 1], [5]];
vConstraints = [[5], [5], [5], [3, 1], [3, 1], [5], [5], [6], [5, 6], [9, 5],
    [11, 5, 1], [13, 6, 1], [14, 6, 1], [7, 12, 1], [6, 1, 11, 1],
    [3, 1, 1, 1, 9, 1], [3, 4, 10], [8, 1, 1, 2, 8, 1], [10, 1, 1, 1, 7, 1],
    [10, 4, 1, 1, 7, 1], [3, 2, 5, 2, 1, 2, 6, 2],
    [3, 2, 4, 2, 1, 1, 4, 1], [2, 6, 3, 1, 1, 1, 1, 1],
    [12, 3, 1, 2, 1, 1, 1], [3, 2, 7, 3, 1, 2, 1, 2],
    [2, 6, 3, 1, 1, 1, 1], [12, 3, 1, 5], [6, 3, 1], [6, 4, 1], [5, 4],
    [4, 1, 1], [5]];

function animate() {
    solver.solveStep();
    if (!solver.isSolved()) setTimeout(animate, animPause);
}

function loader() {
    table = document.getElementById('solver');
    solver = new PuzzleSolver(table, 32, 32, hConstraints, vConstraints);
    setTimeout(animate);
}
window.onload = loader;

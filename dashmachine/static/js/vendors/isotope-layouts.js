/*!
 * cellsByRows layout mode for Isotope
 * v1.1.4
 * https://isotope.metafizzy.co/layout-modes/cellsbyrow.html
 */

/*jshint browser: true, devel: false, strict: true, undef: true, unused: true */

(function (window, factory) {
  // universal module definition
  /* jshint strict: false */ /*globals define, module, require */
  if (typeof define === "function" && define.amd) {
    // AMD
    define(["isotope-layout/js/layout-mode"], factory);
  } else if (typeof exports === "object") {
    // CommonJS
    module.exports = factory(require("isotope-layout/js/layout-mode"));
  } else {
    // browser global
    factory(window.Isotope.LayoutMode);
  }
})(window, function factory(LayoutMode) {
  "use strict";

  var CellsByRow = LayoutMode.create("cellsByRow");
  var proto = CellsByRow.prototype;

  proto._resetLayout = function () {
    // reset properties
    this.itemIndex = 0;
    // measurements
    this.getColumnWidth();
    this.getRowHeight();
    // set cols
    this.cols = Math.floor(this.isotope.size.innerWidth / this.columnWidth);
    this.cols = Math.max(this.cols, 1);
  };

  proto._getItemLayoutPosition = function (item) {
    item.getSize();
    var col = this.itemIndex % this.cols;
    var row = Math.floor(this.itemIndex / this.cols);
    // center item within cell
    var x = (col + 0.5) * this.columnWidth - item.size.outerWidth / 2;
    var y = (row + 0.5) * this.rowHeight - item.size.outerHeight / 2;
    this.itemIndex++;
    return { x: x, y: y };
  };

  proto._getContainerSize = function () {
    return {
      height: Math.ceil(this.itemIndex / this.cols) * this.rowHeight,
    };
  };

  return CellsByRow;
});

/*!
 * masonryHorizontal layout mode for Isotope
 * v2.0.1
 * https://isotope.metafizzy.co/layout-modes/masonryhorizontal.html
 */

/*jshint browser: true, strict: true, undef: true, unused: true */

(function (window, factory) {
  "use strict";
  // universal module definition
  if (typeof define === "function" && define.amd) {
    // AMD
    define(["get-size/get-size", "isotope-layout/js/layout-mode"], factory);
  } else if (typeof module == "object" && module.exports) {
    // CommonJS
    module.exports = factory(
      require("get-size"),
      require("isotope-layout/js/layout-mode")
    );
  } else {
    // browser global
    factory(window.getSize, window.Isotope.LayoutMode);
  }
})(window, function factory(getSize, LayoutMode) {
  "use strict";

  // -------------------------- definition -------------------------- //

  // create an Outlayer layout class
  var MasonryHorizontal = LayoutMode.create("masonryHorizontal");
  var proto = MasonryHorizontal.prototype;

  proto._resetLayout = function () {
    this.getRowHeight();
    this._getMeasurement("gutter", "outerHeight");

    this.rowHeight += this.gutter;
    // measure rows
    this.rows = Math.floor(
      (this.isotope.size.innerHeight + this.gutter) / this.rowHeight
    );
    this.rows = Math.max(this.rows, 1);

    // reset row Xs
    var i = this.rows;
    this.rowXs = [];
    while (i--) {
      this.rowXs.push(0);
    }

    this.maxX = 0;
  };

  proto._getItemLayoutPosition = function (item) {
    item.getSize();
    // how many rows does this brick span
    var remainder = item.size.outerHeight % this.rowHeight;
    var mathMethod = remainder && remainder < 1 ? "round" : "ceil";
    // round if off by 1 pixel, otherwise use ceil
    var rowSpan = Math[mathMethod](item.size.outerHeight / this.rowHeight);
    rowSpan = Math.min(rowSpan, this.rows);

    var rowGroup = this._getRowGroup(rowSpan);
    // get the minimum X value from the rows
    var minimumX = Math.min.apply(Math, rowGroup);
    var shortRowIndex = rowGroup.indexOf(minimumX);

    // position the brick
    var position = {
      x: minimumX,
      y: this.rowHeight * shortRowIndex,
    };

    // apply setHeight to necessary rows
    var setWidth = minimumX + item.size.outerWidth;
    var setSpan = this.rows + 1 - rowGroup.length;
    for (var i = 0; i < setSpan; i++) {
      this.rowXs[shortRowIndex + i] = setWidth;
    }

    return position;
  };

  /**
   * @param {Number} rowSpan - number of rows the element spans
   * @returns {Array} rowGroup
   */
  proto._getRowGroup = function (rowSpan) {
    if (rowSpan < 2) {
      // if brick spans only one row, use all the row Xs
      return this.rowXs;
    }

    var rowGroup = [];
    // how many different places could this brick fit horizontally
    var groupCount = this.rows + 1 - rowSpan;
    // for each group potential horizontal position
    for (var i = 0; i < groupCount; i++) {
      // make an array of rowX values for that one group
      var groupRowXs = this.rowXs.slice(i, i + rowSpan);
      // and get the max value of the array
      rowGroup[i] = Math.max.apply(Math, groupRowXs);
    }
    return rowGroup;
  };

  proto._manageStamp = function (stamp) {
    var stampSize = getSize(stamp);
    var offset = this.isotope._getElementOffset(stamp);
    // get the rows that this stamp affects
    var firstY = this._getOption("originTop") ? offset.top : offset.bottom;
    var lastY = firstY + stampSize.outerHeight;
    var firstRow = Math.floor(firstY / this.rowHeight);
    firstRow = Math.max(0, firstRow);
    var lastRow = Math.floor(lastY / this.rowHeight);
    lastRow = Math.min(this.rows - 1, lastRow);
    // set rowXs to outside edge of the stamp
    var stampMaxX =
      (this._getOption("originLeft") ? offset.left : offset.right) +
      stampSize.outerWidth;
    for (var i = firstRow; i <= lastRow; i++) {
      this.rowXs[i] = Math.max(stampMaxX, this.rowXs[i]);
    }
  };

  proto._getContainerSize = function () {
    this.maxX = Math.max.apply(Math, this.rowXs);

    return {
      width: this.maxX,
    };
  };

  proto.needsResizeLayout = function () {
    return this.needsVerticalResizeLayout();
  };

  return MasonryHorizontal;
});

/*!
 * fitColumns layout mode for Isotope
 * v1.1.4
 * https://isotope.metafizzy.co/layout-modes/fitcolumns.html
 */

/*jshint browser: true, devel: false, strict: true, undef: true, unused: true */

(function (window, factory) {
  // universal module definition
  /* jshint strict: false */ /*globals define, module, require */
  if (typeof define === "function" && define.amd) {
    // AMD
    define(["isotope-layout/js/layout-mode"], factory);
  } else if (typeof exports === "object") {
    // CommonJS
    module.exports = factory(require("isotope-layout/js/layout-mode"));
  } else {
    // browser global
    factory(window.Isotope.LayoutMode);
  }
})(window, function factory(LayoutMode) {
  "use strict";

  var FitColumns = LayoutMode.create("fitColumns");
  var proto = FitColumns.prototype;

  proto._resetLayout = function () {
    this.x = 0;
    this.y = 0;
    this.maxX = 0;
  };

  proto._getItemLayoutPosition = function (item) {
    item.getSize();

    // if this element cannot fit in the current row
    if (
      this.y !== 0 &&
      item.size.outerHeight + this.y > this.isotope.size.innerHeight
    ) {
      this.y = 0;
      this.x = this.maxX;
    }

    var position = {
      x: this.x,
      y: this.y,
    };

    this.maxX = Math.max(this.maxX, this.x + item.size.outerWidth);
    this.y += item.size.outerHeight;

    return position;
  };

  proto._getContainerSize = function () {
    return { width: this.maxX };
  };

  proto.needsResizeLayout = function () {
    return this.needsVerticalResizeLayout();
  };

  return FitColumns;
});

/*!
 * cellsByColumn layout mode for Isotope
 * v1.1.4
 * https://isotope.metafizzy.co/layout-modes/cellsbycolumn.html
 */

/*jshint browser: true, devel: false, strict: true, undef: true, unused: true */

(function (window, factory) {
  // universal module definition
  /* jshint strict: false */ /*globals define, module, require */
  if (typeof define === "function" && define.amd) {
    // AMD
    define(["isotope-layout/js/layout-mode"], factory);
  } else if (typeof exports === "object") {
    // CommonJS
    module.exports = factory(require("isotope-layout/js/layout-mode"));
  } else {
    // browser global
    factory(window.Isotope.LayoutMode);
  }
})(window, function factory(LayoutMode) {
  "use strict";

  var CellsByColumn = LayoutMode.create("cellsByColumn");
  var proto = CellsByColumn.prototype;

  proto._resetLayout = function () {
    // reset properties
    this.itemIndex = 0;
    // measurements
    this.getColumnWidth();
    this.getRowHeight();
    // set rows
    this.rows = Math.floor(this.isotope.size.innerHeight / this.rowHeight);
    this.rows = Math.max(this.rows, 1);
  };

  proto._getItemLayoutPosition = function (item) {
    item.getSize();
    var col = Math.floor(this.itemIndex / this.rows);
    var row = this.itemIndex % this.rows;
    // center item within cell
    var x = (col + 0.5) * this.columnWidth - item.size.outerWidth / 2;
    var y = (row + 0.5) * this.rowHeight - item.size.outerHeight / 2;
    this.itemIndex++;
    return { x: x, y: y };
  };

  proto._getContainerSize = function () {
    return {
      width: Math.ceil(this.itemIndex / this.rows) * this.columnWidth,
    };
  };

  proto.needsResizeLayout = function () {
    return this.needsVerticalResizeLayout();
  };

  return CellsByColumn;
});

/*!
 * horizontal layout mode for Isotope
 * v2.0.1
 * https://isotope.metafizzy.co/layout-modes/horiz.html
 */

(function (window, factory) {
  // universal module definition
  /* jshint strict: false */ /*globals define, module, require */
  if (typeof define === "function" && define.amd) {
    // AMD
    define(["isotope-layout/js/layout-mode"], factory);
  } else if (typeof module == "object" && module.exports) {
    // CommonJS
    module.exports = factory(require("isotope-layout/js/layout-mode"));
  } else {
    // browser global
    factory(window.Isotope.LayoutMode);
  }
})(window, function factory(LayoutMode) {
  "use strict";

  var Horiz = LayoutMode.create("horiz", {
    verticalAlignment: 0,
  });

  var proto = Horiz.prototype;

  proto._resetLayout = function () {
    this.x = 0;
  };

  proto._getItemLayoutPosition = function (item) {
    item.getSize();
    var y =
      (this.isotope.size.innerHeight - item.size.outerHeight) *
      this.options.verticalAlignment;
    var x = this.x;
    this.x += item.size.outerWidth;
    return { x: x, y: y };
  };

  proto._getContainerSize = function () {
    return { width: this.x };
  };

  proto.needsResizeLayout = function () {
    return this.needsVerticalResizeLayout();
  };

  return Horiz;
});
